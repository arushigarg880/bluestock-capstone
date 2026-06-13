import pandas as pd
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent.parent

sip   = pd.read_csv(BASE / "data/raw/04_monthly_sip_inflows.csv")
fund  = pd.read_csv(BASE / "data/raw/01_fund_master.csv")
score = pd.read_csv(BASE / "data/processed/fund_scorecard.csv")

top5 = score.nlargest(5, 'composite_score')[
    ['scheme_name','fund_house','composite_score','cagr_3yr','sharpe_ratio']].copy()

latest_sip  = sip['sip_inflow_crore'].iloc[-1]
prev_sip    = sip['sip_inflow_crore'].iloc[-2]
sip_growth  = ((latest_sip - prev_sip) / prev_sip * 100)
date_str    = datetime.now().strftime("%d %B %Y")

def make_fund_rows(df):
    rows = ""
    colors = ['#E6F1FB','#EAF3DE','#EEEDFE','#FAEEDA','#FAECE7']
    for i, (_, row) in enumerate(df.iterrows()):
        bg = colors[i % len(colors)]
        rows += f"""
        <tr style="background:{bg}">
          <td style="padding:10px 14px;font-weight:500;color:#1a1a1a">{i+1}. {row['scheme_name'][:35]}</td>
          <td style="padding:10px 14px;color:#444">{row['fund_house'][:20]}</td>
          <td style="padding:10px 14px;text-align:center;font-weight:500;color:#0F6E56">{row['cagr_3yr']:.1f}%</td>
          <td style="padding:10px 14px;text-align:center;color:#185FA5">{row['sharpe_ratio']:.2f}</td>
          <td style="padding:10px 14px;text-align:center;font-weight:500;color:#534AB7">{row['composite_score']:.1f}</td>
        </tr>"""
    return rows

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Bluestock Fintech Weekly Report</title>
</head>
<body style="margin:0;padding:0;background:#F4F4F7;font-family:Arial,sans-serif">

<table width="100%" cellpadding="0" cellspacing="0" style="background:#F4F4F7;padding:30px 0">
<tr><td align="center">
<table width="620" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden">

  <!-- HEADER -->
  <tr>
    <td style="background:#1F3864;padding:28px 32px">
      <h1 style="color:#ffffff;margin:0;font-size:22px">Bluestock Fintech</h1>
      <p style="color:#B5D4F4;margin:6px 0 0;font-size:14px">Weekly Mutual Fund Performance Report — {date_str}</p>
    </td>
  </tr>

  <!-- KPI CARDS -->
  <tr>
    <td style="padding:24px 32px 8px">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td width="31%" style="background:#E6F1FB;border-radius:8px;padding:16px;text-align:center">
            <p style="margin:0;font-size:11px;color:#185FA5;text-transform:uppercase">Industry AUM</p>
            <p style="margin:6px 0 0;font-size:22px;font-weight:700;color:#0C447C">Rs.81 L Cr</p>
          </td>
          <td width="4%"></td>
          <td width="31%" style="background:#E1F5EE;border-radius:8px;padding:16px;text-align:center">
            <p style="margin:0;font-size:11px;color:#0F6E56;text-transform:uppercase">Monthly SIP</p>
            <p style="margin:6px 0 0;font-size:22px;font-weight:700;color:#085041">Rs.{latest_sip:,.0f} Cr</p>
            <p style="margin:4px 0 0;font-size:11px;color:#1D9E75">{'Up' if sip_growth>0 else 'Down'} {abs(sip_growth):.1f}% MoM</p>
          </td>
          <td width="4%"></td>
          <td width="31%" style="background:#EEEDFE;border-radius:8px;padding:16px;text-align:center">
            <p style="margin:0;font-size:11px;color:#534AB7;text-transform:uppercase">Total Folios</p>
            <p style="margin:6px 0 0;font-size:22px;font-weight:700;color:#3C3489">26.12 Cr</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- TOP FUNDS TABLE -->
  <tr>
    <td style="padding:24px 32px 8px">
      <h2 style="margin:0 0 14px;font-size:16px;color:#1F3864;border-bottom:2px solid #E6F1FB;padding-bottom:8px">Top 5 Funds This Week</h2>
      <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px">
        <tr style="background:#1F3864">
          <th style="padding:10px 14px;color:#fff;text-align:left;font-weight:500">Fund Name</th>
          <th style="padding:10px 14px;color:#fff;text-align:left;font-weight:500">AMC</th>
          <th style="padding:10px 14px;color:#fff;text-align:center;font-weight:500">3yr CAGR</th>
          <th style="padding:10px 14px;color:#fff;text-align:center;font-weight:500">Sharpe</th>
          <th style="padding:10px 14px;color:#fff;text-align:center;font-weight:500">Score</th>
        </tr>
        {make_fund_rows(top5)}
      </table>
    </td>
  </tr>

  <!-- INSIGHT BOX -->
  <tr>
    <td style="padding:20px 32px">
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td style="background:#FFF8E6;border-left:4px solid #BA7517;border-radius:0 8px 8px 0;padding:14px 16px">
            <p style="margin:0;font-size:13px;font-weight:700;color:#633806">Weekly Insight</p>
            <p style="margin:6px 0 0;font-size:13px;color:#854F0B;line-height:1.6">
              SIP inflows {'increased' if sip_growth>0 else 'decreased'} by {abs(sip_growth):.1f}% this month.
              The top ranked fund is <strong>{top5.iloc[0]['scheme_name'][:35]}</strong>
              with a 3-year CAGR of {top5.iloc[0]['cagr_3yr']:.1f}% and
              composite score of {top5.iloc[0]['composite_score']:.1f}.
            </p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="background:#F4F4F7;padding:20px 32px;text-align:center">
      <p style="margin:0;font-size:12px;color:#888">Auto-generated by Bluestock Fintech ETL Pipeline.</p>
      <p style="margin:4px 0 0;font-size:12px;color:#888">Data sourced from AMFI India. For internal use only.</p>
    </td>
  </tr>

</table>
</td></tr>
</table>
</body>
</html>"""

output_path = BASE / "reports/weekly_report.html"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Report saved → {output_path}")
print("Open reports/weekly_report.html in your browser to preview!")