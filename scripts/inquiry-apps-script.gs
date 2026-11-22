/**
 * Aikhoje Studios — website inquiry handler (Google Apps Script web app).
 *
 * Receives the wedding inquiry form and the real-estate booking form from
 * aikhojestudios.com, then:
 *   1. emails the inquiry to the studio inbox (Reply goes straight to the client),
 *   2. sends the client an auto-reply from the studio's own Gmail,
 *   3. logs every submission to the "Website inquiries" Google Sheet.
 *
 * Deployed as an Apps Script web app (Execute as: the studio account; Who has access: Anyone).
 * Paste its /exec URL into FORM_ENDPOINT in scripts/build-site.py and the real-estate form.
 */

var STUDIO_EMAIL = 'aikhojestudios@gmail.com';
var STUDIO_NAME = 'Aikhoje Studios';
var SHEET_NAME = 'Website inquiries';
// The "Aikhoje Studios — Website inquiries" spreadsheet in the studio Google Drive.
var SHEET_ID = '1-awmMc5HVsPIqKuG96tvDDh926bsug-HijFUIOEFoWQ';
// Only these sites may submit (stops strangers using the endpoint from elsewhere).
var ALLOWED_PAGES = /^https:\/\/(www\.)?aikhojestudios\.com\//;

function doPost(e) {
  try {
    var data = JSON.parse((e && e.postData && e.postData.contents) || '{}');

    // Spam traps: real visitors never see or fill the hidden fields.
    if (data._honey || data._website) return json_({ success: true });

    var page = String(data._page || '');
    if (page && !ALLOWED_PAGES.test(page)) return json_({ success: false, error: 'origin' });

    // Bot check: suspected bots get a normal "success" reply (so they move on), but no email,
    // no auto-reply — they're only logged to the "Blocked" tab of the sheet so nothing real is lost.
    var reasons = botReasons_(data);
    if (reasons.length >= 2) {
      logBlocked_(page, data, reasons);
      return json_({ success: true });
    }

    var clientEmail = String(data.email || data.Email || '').trim();
    var clientName = String(data.Name || '').trim();
    if (!clientName || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(clientEmail)) {
      return json_({ success: false, error: 'missing name or email' });
    }

    // Light rate limit: at most 5 submissions per email address per hour.
    var cache = CacheService.getScriptCache();
    var key = 'n:' + clientEmail.toLowerCase();
    var n = Number(cache.get(key) || 0);
    if (n >= 5) return json_({ success: false, error: 'rate' });
    cache.put(key, String(n + 1), 3600);

    var subject = String(data._subject || 'New inquiry from your website');
    var autoreply = String(data._autoresponse || '');
    var fields = Object.keys(data).filter(function (k) { return k.charAt(0) !== '_'; });
    if (reasons.length) subject = '[Check: possible spam] ' + subject;

    // 1. Email to the studio.
    var rows = fields.map(function (k) {
      return '<tr><td style="padding:6px 12px;border:1px solid #ddd;background:#f6f4ee;font-weight:600;vertical-align:top">' +
        esc_(k) + '</td><td style="padding:6px 12px;border:1px solid #ddd;white-space:pre-wrap">' + esc_(data[k]) + '</td></tr>';
    }).join('');
    var html = '<p style="font-family:Arial,sans-serif">New submission from <a href="' + esc_(page) + '">' + esc_(page || 'your website') + '</a>. ' +
      'Hit Reply to answer ' + esc_(clientName) + ' directly.</p>' +
      '<table style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:14px">' + rows + '</table>';
    var text = fields.map(function (k) { return k + ': ' + data[k]; }).join('\n');
    GmailApp.sendEmail(STUDIO_EMAIL, subject, text, { htmlBody: html, replyTo: clientEmail, name: 'Website · ' + clientName });

    // 2. Auto-reply to the client, from the studio's own Gmail (skipped if anything looked off).
    if (autoreply && !reasons.length) {
      GmailApp.sendEmail(clientEmail, 'Thank you for reaching out to ' + STUDIO_NAME, autoreply, {
        name: STUDIO_NAME,
        replyTo: STUDIO_EMAIL
      });
    }

    // 3. Log to the sheet.
    log_(subject, page, data, fields);

    return json_({ success: true });
  } catch (err) {
    console.error(err);
    return json_({ success: false, error: 'server' });
  }
}

/**
 * Signs that a submission came from a bot rather than a couple or an agent. Two or more = blocked;
 * one = still delivered, but flagged in the subject and no auto-reply is sent.
 */
function botReasons_(data) {
  var r = [];
  var t = Number(data._t);
  if (!t) r.push('no timing (posted without the page)');
  else if (t < 3000) r.push('filled in under 3 seconds');

  var name = String(data.Name || '');
  if (gibberish_(name)) r.push('random-letter name');

  var textKeys = ['Ceremony Location', 'About Their Day', 'Brokerage', 'Property Address', 'Notes'];
  if (textKeys.some(function (k) { return gibberish_(String(data[k] || '')); })) r.push('random-letter text');

  ['Wedding Date', 'Preferred Shoot Date'].forEach(function (k) {
    var m = String(data[k] || '').match(/^(\d{4})-\d{2}-\d{2}$/);
    if (m && Number(m[1]) < new Date().getFullYear() - 1) r.push('date in the distant past');
  });

  var local = String(data.email || '').split('@')[0];
  if ((local.match(/\./g) || []).length >= 3) r.push('dotted throwaway email');
  return r;
}

// One long "word" of letters that flips between upper and lower case many times, e.g. KnAGfzUdBsXgqs.
function gibberish_(s) {
  s = s.trim();
  if (s.length < 10 || /\s/.test(s) || !/^[A-Za-z]+$/.test(s)) return false;
  var flips = 0;
  for (var i = 1; i < s.length; i++) {
    if ((s[i] === s[i].toUpperCase()) !== (s[i - 1] === s[i - 1].toUpperCase())) flips++;
  }
  return flips >= 5;
}

function logBlocked_(page, data, reasons) {
  var ss = getSheet_();
  var sh = ss.getSheetByName('Blocked') || ss.insertSheet('Blocked');
  if (!sh.getLastRow()) { sh.appendRow(['Received', 'Page', 'Why', 'Submission']); sh.setFrozenRows(1); }
  var fields = Object.keys(data).filter(function (k) { return k.charAt(0) !== '_'; });
  sh.appendRow([new Date(), page, reasons.join('; '), fields.map(function (k) { return k + ': ' + data[k]; }).join('\n')]);
}

// Visiting the web app URL in a browser shows this, which confirms the deployment is live.
function doGet() {
  return json_({ ok: true, service: 'Aikhoje Studios inquiry form' });
}

function log_(subject, page, data, fields) {
  var ss = getSheet_();
  var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  var headers = sh.getLastRow() ? sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0] : [];
  if (!headers.length) {
    headers = ['Received', 'Form', 'Page'];
    sh.appendRow(headers);
    sh.setFrozenRows(1);
  }
  fields.forEach(function (k) {
    if (headers.indexOf(k) === -1) {
      headers.push(k);
      sh.getRange(1, headers.length).setValue(k);
    }
  });
  var row = headers.map(function (h) {
    if (h === 'Received') return new Date();
    if (h === 'Form') return subject;
    if (h === 'Page') return page;
    return data[h] == null ? '' : String(data[h]);
  });
  sh.appendRow(row);
}

function getSheet_() {
  return SpreadsheetApp.openById(SHEET_ID);
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function esc_(s) {
  return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
  });
}

/** Run once from the editor ("Run" ▸ testSetup) to grant permissions and send yourself a test. */
function testSetup() {
  var res = doPost({ postData: { contents: JSON.stringify({
    _subject: 'TEST – inquiry form setup',
    _page: 'https://aikhojestudios.com/',
    _autoresponse: 'This is the auto-reply couples will receive.',
    _t: 30000,
    Name: 'TEST – setup check',
    email: STUDIO_EMAIL,
    'About Their Day': 'If you can read this, the new inquiry form works.'
  }) } });
  Logger.log(res.getContent());
}
