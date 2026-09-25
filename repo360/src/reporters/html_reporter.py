"""
HTML Dashboard Generator - Creates beautiful interactive dashboard
"""

import json
from pathlib import Path
from datetime import datetime

class HTMLDashboardGenerator:
    """Generates interactive HTML dashboard"""
    
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
    
    def generate(self, results):
        """Generate HTML dashboard"""
        
        html = self._build_html(results)
        
        output_file = self.output_dir / 'dashboard.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✓ Dashboard generated: {output_file}")
    
    def _build_html(self, results):
        """Build complete HTML - THIS IS THE REAL DASHBOARD FOR PROJECT MANAGERS"""
        
        scores = results.get('scores', {})
        stats = results.get('statistics', {})
        metrics = results.get('metrics', {})
        security = results.get('security', {})
        repo_info = results.get('repository', {})
        
        # Calculate issue counts
        all_issues = []
        for file_result in results.get('files', []):
            all_issues.extend(file_result.get('issues', []))
        
        critical_issues = [i for i in all_issues if i.get('severity') == 'critical']
        high_issues = [i for i in all_issues if i.get('severity') == 'high']
        medium_issues = [i for i in all_issues if i.get('severity') == 'medium']
        low_issues = [i for i in all_issues if i.get('severity') == 'low']
        
        # Add security issues
        critical_issues.extend(security.get('secrets', []))
        for vuln in security.get('vulnerabilities', []):
            if vuln['severity'] == 'critical':
                critical_issues.append(vuln)
            elif vuln['severity'] == 'high':
                high_issues.append(vuln)
            elif vuln['severity'] == 'medium':
                medium_issues.append(vuln)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Repo360 Analysis Dashboard - Project Health</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f7fa;
            color: #2c3e50;
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header .repo-info {{
            opacity: 0.9;
            font-size: 0.95rem;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .score-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .score-card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .score-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }}
        
        .score-card h3 {{
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #7f8c8d;
            margin-bottom: 0.5rem;
        }}
        
        .score-value {{
            font-size: 3rem;
            font-weight: bold;
            margin: 0.5rem 0;
        }}
        
        .score-excellent {{ color: #27ae60; }}
        .score-good {{ color: #2ecc71; }}
        .score-fair {{ color: #f39c12; }}
        .score-poor {{ color: #e74c3c; }}
        .score-critical {{ color: #c0392b; }}
        
        .score-bar {{
            height: 8px;
            background: #ecf0f1;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 1rem;
        }}
        
        .score-fill {{
            height: 100%;
            transition: width 1s ease;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .stat-box {{
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }}
        
        .section {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        
        .section h2 {{
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #ecf0f1;
            color: #2c3e50;
        }}
        
        .issue-list {{
            list-style: none;
        }}
        
        .issue-item {{
            padding: 1rem;
            margin-bottom: 0.75rem;
            border-left: 4px solid #e74c3c;
            background: #fff5f5;
            border-radius: 4px;
        }}
        
        .issue-item.critical {{
            border-left-color: #c0392b;
            background: #ffebee;
        }}
        
        .issue-item.high {{
            border-left-color: #e74c3c;
            background: #fff5f5;
        }}
        
        .issue-item.medium {{
            border-left-color: #f39c12;
            background: #fff9e6;
        }}
        
        .issue-item.low {{
            border-left-color: #3498db;
            background: #f0f8ff;
        }}
        
        .issue-type {{
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.5px;
        }}
        
        .issue-message {{
            margin-top: 0.5rem;
            color: #555;
        }}
        
        .issue-location {{
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: #7f8c8d;
            font-family: 'Courier New', monospace;
        }}
        
        .language-chart {{
            display: flex;
            height: 40px;
            border-radius: 8px;
            overflow: hidden;
            margin: 1rem 0;
        }}
        
        .language-segment {{
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        .language-segment:hover {{
            filter: brightness(1.1);
        }}
        
        .legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        
        .badge-critical {{ background: #ffebee; color: #c0392b; }}
        .badge-high {{ background: #fff5f5; color: #e74c3c; }}
        .badge-medium {{ background: #fff9e6; color: #f39c12; }}
        .badge-low {{ background: #f0f8ff; color: #3498db; }}
        
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #7f8c8d;
            font-size: 0.9rem;
        }}
        
        @media (max-width: 768px) {{
            .score-grid {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 1.8rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>🎯 Repo360 Analysis Dashboard</h1>
            <div class="repo-info">
                <strong>{repo_info.get('url', 'Unknown Repository')}</strong> • 
                Branch: {repo_info.get('branch', 'N/A')} • 
                Analyzed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
    </div>
    
    <div class="container">
        <!-- Overall Scores -->
        <div class="score-grid">
            {self._generate_score_card('Overall Score', scores.get('overall', 0), 'The overall health score of your codebase')}
            {self._generate_score_card('Quality', scores.get('quality', 0), 'Code quality and maintainability')}
            {self._generate_score_card('Security', scores.get('security', 0), 'Security vulnerabilities and risks')}
            {self._generate_score_card('Complexity', scores.get('complexity', 0), 'Code complexity metrics')}
        </div>
        
        <!-- Statistics -->
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-number">{stats.get('total_files', 0)}</div>
                <div class="stat-label">Source Files</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(critical_issues)}</div>
                <div class="stat-label">Critical Issues</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(high_issues)}</div>
                <div class="stat-label">High Issues</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(medium_issues)}</div>
                <div class="stat-label">Medium Issues</div>
            </div>
        </div>
        
        <!-- Language Distribution -->
        <div class="section">
            <h2>📊 Language Distribution</h2>
            {self._generate_language_chart(stats.get('languages', {}))}
        </div>
        
        <!-- Critical Issues -->
        {self._generate_issues_section('🔥 Critical Issues', critical_issues, 'critical')}
        
        <!-- High Priority Issues -->
        {self._generate_issues_section('⚠️ High Priority Issues', high_issues, 'high')}
        
        <!-- Security Findings -->
        {self._generate_security_section(security)}
        
        <!-- Metrics Summary -->
        {self._generate_metrics_section(metrics)}
    </div>
    
    <div class="footer">
        Generated by Repo360 • Enterprise Code Analysis Platform
    </div>
</body>
</html>"""
    
    def _generate_score_card(self, title, score, description):
        """Generate a score card"""
        
        score = round(score, 1)
        
        if score >= 90:
            color_class = 'score-excellent'
            color = '#27ae60'
        elif score >= 75:
            color_class = 'score-good'
            color = '#2ecc71'
        elif score >= 60:
            color_class = 'score-fair'
            color = '#f39c12'
        elif score >= 40:
            color_class = 'score-poor'
            color = '#e74c3c'
        else:
            color_class = 'score-critical'
            color = '#c0392b'
        
        return f"""
            <div class="score-card">
                <h3>{title}</h3>
                <div class="score-value {color_class}">{score}</div>
                <div class="score-bar">
                    <div class="score-fill" style="width: {score}%; background: {color};"></div>
                </div>
                <p style="margin-top: 0.75rem; color: #7f8c8d; font-size: 0.85rem;">{description}</p>
            </div>
        """
    
    def _generate_language_chart(self, languages):
        """Generate language distribution chart"""
        
        if not languages:
            return "<p>No languages detected</p>"
        
        colors = {
            'java': '#b07219',
            'python': '#3572A5',
            'javascript': '#f1e05a',
            'typescript': '#2b7489',
            'go': '#00ADD8',
            'ruby': '#701516',
            'php': '#4F5D95',
            'csharp': '#178600',
            'cpp': '#f34b7d',
            'rust': '#dea584'
        }
        
        chart_html = '<div class="language-chart">'
        legend_html = '<div class="legend">'
        
        for lang, data in sorted(languages.items(), key=lambda x: x[1].get('percentage', 0), reverse=True):
            percentage = data.get('percentage', 0)
            if percentage > 0:
                color = colors.get(lang.lower(), '#95a5a6')
                chart_html += f'<div class="language-segment" style="width: {percentage}%; background: {color};" title="{lang}: {percentage}%">'
                if percentage > 10:
                    chart_html += f'{percentage:.1f}%'
                chart_html += '</div>'
                
                legend_html += f'''
                    <div class="legend-item">
                        <div class="legend-color" style="background: {color};"></div>
                        <span>{lang.title()}: {data.get('files', 0)} files ({percentage:.1f}%)</span>
                    </div>
                '''
        
        chart_html += '</div>'
        legend_html += '</div>'
        
        return chart_html + legend_html
    
    def _generate_issues_section(self, title, issues, severity):
        """Generate issues section"""
        
        if not issues:
            return f'''
                <div class="section">
                    <h2>{title}</h2>
                    <p style="color: #27ae60; font-weight: 600;">✓ No {severity} issues found!</p>
                </div>
            '''
        
        issues_html = '<ul class="issue-list">'
        for issue in issues[:20]:  # Show first 20
            issues_html += f'''
                <li class="issue-item {severity}">
                    <div class="issue-type">{issue.get('type', 'Unknown').replace('_', ' ')}</div>
                    <div class="issue-message">{issue.get('message', 'No description')}</div>
                    <div class="issue-location">📁 {issue.get('file', 'Unknown file')}:{issue.get('line', '?')}</div>
                </li>
            '''
        
        if len(issues) > 20:
            issues_html += f'<li style="padding: 1rem; text-align: center; color: #7f8c8d;">... and {len(issues) - 20} more issues</li>'
        
        issues_html += '</ul>'
        
        return f'''
            <div class="section">
                <h2>{title} <span class="badge badge-{severity}">{len(issues)}</span></h2>
                {issues_html}
            </div>
        '''
    
    def _generate_security_section(self, security):
        """Generate security section"""
        
        secrets = security.get('secrets', [])
        vulns = security.get('vulnerabilities', [])
        
        if not secrets and not vulns:
            return f'''
                <div class="section">
                    <h2>🔒 Security Scan</h2>
                    <p style="color: #27ae60; font-weight: 600;">✓ No security issues detected!</p>
                </div>
            '''
        
        content = '<div class="stats-grid">'
        content += f'<div class="stat-box"><div class="stat-number">{len(secrets)}</div><div class="stat-label">Secrets Found</div></div>'
        content += f'<div class="stat-box"><div class="stat-number">{len(vulns)}</div><div class="stat-label">Vulnerabilities</div></div>'
        content += f'<div class="stat-box"><div class="stat-number">{security.get("critical_count", 0)}</div><div class="stat-label">Critical</div></div>'
        content += f'<div class="stat-box"><div class="stat-number">{security.get("high_count", 0)}</div><div class="stat-label">High</div></div>'
        content += '</div>'
        
        return f'''
            <div class="section">
                <h2>🔒 Security Scan</h2>
                {content}
            </div>
        '''
    
    def _generate_metrics_section(self, metrics):
        """Generate metrics summary"""
        
        complexity = metrics.get('complexity', {})
        quality = metrics.get('quality', {})
        
        return f'''
            <div class="section">
                <h2>📈 Metrics Summary</h2>
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-number">{complexity.get('average_complexity', 0):.1f}</div>
                        <div class="stat-label">Avg Complexity</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{quality.get('maintainability_average', 0):.1f}</div>
                        <div class="stat-label">Maintainability Index</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{metrics.get('technical_debt', {}).get('total_hours', 0):.0f}h</div>
                        <div class="stat-label">Technical Debt</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">${metrics.get('technical_debt', {}).get('total_cost', 0):,.0f}</div>
                        <div class="stat-label">Debt Cost</div>
                    </div>
                </div>
            </div>
        '''
