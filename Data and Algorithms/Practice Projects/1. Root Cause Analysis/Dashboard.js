import React, { useState } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const KYCMonitoringDashboard = () => {
  const [selectedTeam, setSelectedTeam] = useState('kyc-verification');
  const [dateRange, setDateRange] = useState('last-8-weeks');
  const [activeTab, setActiveTab] = useState('health');

  // Mock data
  const passRateData = [
    { week: '2017-05', passRate: 82.8 },
    { week: '2017-06', passRate: 90.9 },
    { week: '2017-07', passRate: 84.5 },
    { week: '2017-08', passRate: 79.0 },
    { week: '2017-09', passRate: 69.7 },
    { week: '2017-10', passRate: 58.7 },
  ];

  const alertsData = [
    { date: 'Oct 1', alerts: 2 },
    { date: 'Oct 8', alerts: 0 },
    { date: 'Oct 15', alerts: 1 },
    { date: 'Oct 22', alerts: 4 },
    { date: 'Oct 29', alerts: 11 },
    { date: 'Nov 5', alerts: 8 },
    { date: 'Nov 12', alerts: 6 },
    { date: 'Nov 19', alerts: 7 },
  ];

  const subCheckHealth = [
    {
      check: 'image_integrity_result',
      project: 'document-verification',
      last8w: 74.2,
      last7d: 61.7,
      difference: -12.5,
      status: 'critical',
      bars: [1,1,1,1,1,1,1,0,0,0]
    },
    {
      check: 'image_quality_result',
      project: 'document-verification',
      last8w: 83.2,
      last7d: 79.8,
      difference: -3.4,
      status: 'warning',
      bars: [1,1,1,1,1,1,1,1,0,0]
    },
    {
      check: 'visual_authenticity_result',
      project: 'document-verification',
      last8w: 98.5,
      last7d: 98.3,
      difference: -0.2,
      status: 'healthy',
      bars: [1,1,1,1,1,1,1,1,1,1]
    },
    {
      check: 'face_detection_result',
      project: 'document-verification',
      last8w: 99.5,
      last7d: 99.6,
      difference: 0.1,
      status: 'healthy',
      bars: [1,1,1,1,1,1,1,1,1,1]
    },
    {
      check: 'face_comparison_result',
      project: 'face-verification',
      last8w: 99.7,
      last7d: 99.8,
      difference: 0.1,
      status: 'healthy',
      bars: [1,1,1,1,1,1,1,1,1,1]
    },
    {
      check: 'facial_image_integrity_result',
      project: 'face-verification',
      last8w: 95.2,
      last7d: 97.3,
      difference: 2.1,
      status: 'improving',
      bars: [1,1,1,1,1,1,1,1,1,1]
    },
  ];

  const keyTransactions = [
    {
      transaction: '/api/v2/kyc/document/verify',
      project: 'document-verification',
      last8w: 89.2,
      last7d: 61.7,
      change: '-27.5% worse',
      bars8w: [1,1,1,1,1,1,1,1,0,0],
      bars7d: [1,1,0,0,0,0,0,0,0,0]
    },
    {
      transaction: '/api/v2/kyc/face/verify',
      project: 'face-verification',
      last8w: 96.1,
      last7d: 97.3,
      change: '1.2% better',
      bars8w: [1,1,1,1,1,1,1,1,1,1],
      bars7d: [1,1,1,1,1,1,1,1,1,1]
    },
    {
      transaction: '/api/v2/kyc/complete',
      project: 'kyc-orchestrator',
      last8w: 84.5,
      last7d: 58.7,
      change: '-25.8% worse',
      bars8w: [1,1,1,1,1,1,1,0,0,0],
      bars7d: [1,1,0,0,0,0,0,0,0,0]
    },
  ];

  const alertRules = [
    {
      rule: 'Pass Rate Below 75%',
      project: 'kyc-orchestrator',
      last8wAvg: 3.2,
      thisWeek: 12,
      difference: '+8.8'
    },
    {
      rule: 'image_integrity Degradation',
      project: 'document-verification',
      last8wAvg: 1.8,
      thisWeek: 9,
      difference: '+7.2'
    },
    {
      rule: 'Document Rejection Spike',
      project: 'document-verification',
      last8wAvg: 2.1,
      thisWeek: 6,
      difference: '+3.9'
    },
  ];

  const getStatusColor = (status) => {
    switch(status) {
      case 'critical': return '#f55459';
      case 'warning': return '#f5a623';
      case 'healthy': return '#3fb950';
      case 'improving': return '#1f6feb';
      default: return '#6e7781';
    }
  };

  const getChangeColor = (change) => {
    if (change.includes('worse')) return '#f55459';
    if (change.includes('better')) return '#3fb950';
    return '#6e7781';
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1fa9f4 0%, #6ee7fc 50%, #ffffff 100%)',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      {/* Sidebar */}
      <div style={{
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        width: '220px',
        background: '#1e1e1e',
        padding: '1rem 0',
        color: 'white'
      }}>
        <div style={{ padding: '0 1rem 2rem 1rem', borderBottom: '1px solid #333' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '6px',
              background: 'linear-gradient(135deg, #1fa9f4, #6ee7fc)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.2rem'
            }}>
              ✓
            </div>
            <div>
              <div style={{ fontWeight: '600', fontSize: '0.95rem' }}>KYC Verification</div>
              <div style={{ fontSize: '0.8rem', color: '#888' }}>Monitoring</div>
            </div>
          </div>
        </div>

        <nav style={{ padding: '1rem 0' }}>
          <NavItem icon="📊" label="Projects" />
          <NavItem icon="⚠️" label="Issues" />
          <NavItem icon="⚡" label="Performance" />
          <NavItem icon="📦" label="Releases" />
          <NavItem icon="🔔" label="Alerts" />
          <NavItem icon="🔍" label="Discover" />
          <NavItem icon="📈" label="Dashboards" />
          <NavItem icon="📋" label="Stats" active />
          <NavItem icon="⚙️" label="Settings" />
        </nav>
      </div>

      {/* Main Content */}
      <div style={{ marginLeft: '220px', padding: '2rem' }}>
        {/* Header */}
        <div style={{
          background: 'rgba(255,255,255,0.95)',
          borderRadius: '8px',
          padding: '1.5rem',
          marginBottom: '1.5rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h1 style={{
              margin: 0,
              fontSize: '1.8rem',
              fontWeight: '600',
              color: '#1e1e1e'
            }}>
              Stats
            </h1>
            <img
              src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAAAYCAYAAABR8BK1AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMySURBVHgB7ZnNThNRFMf/504fKGAppYCxJiSKG1wYE+PChRtde4NuvIE+gT6BPoE+gT6BvoE+gW7cuNAYE0JcGBODQqHQTmnndvr5nzOdGQqdtjOdmbbE/pJJZ+49c8/v3nPvuWcuwP8sWZYxMTGBeDwOv9+PQCCAQCBwruM4DmzbRqvVQrvdRrPZRL1eR7VaRaVSQalUQqFQQC6Xw8HBAfL5PBzH+f+AZhiGUSwWo2QySeVyOcrlchSLxSgSiVAwGCQApwEej4cYhqFgMEh+v5/m5+dpYWGBUqkU3b9/nx48eECrq6u0tbVF2WyW9vf3aW9vj3K5HH348IF+/PhB3759I8MwznV+D4Cuq6urVK/XqVqt0snJCTUaDTKt+7uu67qupdZ1Xdu27Z0O3a7rUqvVolarhWq1Snt7e7S9vU1fv36lbDZLX758od3dXfrw4QMVCgXa3d2lYrFI+Xye9vf3yeVwBLSiKFhbW8PExATi8TjC4TCi0SiCwSACgQBCoRBCoRD8fj98Ph+8Xi88Hg/cbjdkWYYkSTg9vCQJ/f5fEO/t9f7rdDpwHAftdhvNZhP1eh21Wg3VahWlUgmlUgn7+/sol8sol8twXRf5fB4HBwdEREilUmAYBiqVCjRNg6qqUBQFiqJA1/W+7z0A2jAMlEolqh0xDHO+cw+ABgBZlqGqKhKJBObm5rC0tISZmRlMT09jcnISiUQCmqZheHgYyWQSMzMzmJ6eRiKRwNDQEIaGhqBpGjRNg67rUBQFg8PDUBTFi/xtcITOe1bqrYsQ/b8xtLY8w7Ys9UjEUldXV6BWq6FarULXdSiKAkVRoKoqNE2DruvQdR1DQ0PQNA2jo6MYGxvD+Pg4JicnkUqlsLCwgPn5eSwuLuLRo0dYWlrC0tISHj9+jOXlZSwvL+PJkyd4+vQpnj17hufPn2NtbQ2ZTAavXr1CJpPBmzdv8Pr1a7x9+xbv3r3D+/fv8f79e3z8+BGfPn3C58+fkcvlkMvlsLOzg52dHayvrwPo3oPW1taQyWSQzWaRz+eRzWaRy+VQKBRQLBZRLBZRLBZRKpWwv7+PcrmMXC4Hy7I8B93BsizYto1Wq4VmswnXdbsPuuu6aLfbaDQa0HUdsixDkiR4PB54vV54vV54vV74fD5wHAee43D58mW4XC7IsgxJkuByue7MCf8Cf/dW+7GQObQAAAAASUVORK5CYII="
              alt="LightWork AI"
              style={{ height: '30px' }}
            />
          </div>

          {/* Tabs */}
          <div style={{ display: 'flex', gap: '2rem', borderBottom: '1px solid #e0e0e0', marginBottom: '1rem' }}>
            <Tab label="Usage" active={activeTab === 'usage'} onClick={() => setActiveTab('usage')} />
            <Tab label="Issues" active={activeTab === 'issues'} onClick={() => setActiveTab('issues')} />
            <Tab label="Health" active={activeTab === 'health'} onClick={() => setActiveTab('health')} />
          </div>

          {/* Filters */}
          <div style={{ display: 'flex', gap: '1rem' }}>
            <select
              value={selectedTeam}
              onChange={(e) => setSelectedTeam(e.target.value)}
              style={{
                padding: '0.5rem 2rem 0.5rem 0.75rem',
                borderRadius: '6px',
                border: '1px solid #d0d7de',
                fontSize: '0.9rem',
                background: 'white',
                cursor: 'pointer'
              }}
            >
              <option value="kyc-verification">Team: KYC Verification</option>
              <option value="document-team">Team: Document Team</option>
              <option value="face-team">Team: Face Team</option>
            </select>

            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              style={{
                padding: '0.5rem 2rem 0.5rem 0.75rem',
                borderRadius: '6px',
                border: '1px solid #d0d7de',
                fontSize: '0.9rem',
                background: 'white',
                cursor: 'pointer'
              }}
            >
              <option value="last-8-weeks">Date Range: Last 8 weeks</option>
              <option value="last-4-weeks">Date Range: Last 4 weeks</option>
              <option value="last-month">Date Range: Last month</option>
            </select>
          </div>
        </div>

        {/* Monthly Pass Rate Decline Chart */}
        <div style={{
          background: 'rgba(255,255,255,0.95)',
          borderRadius: '8px',
          padding: '2rem',
          marginBottom: '1.5rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{
            margin: '0 0 1.5rem 0',
            fontSize: '1.5rem',
            fontWeight: '600',
            color: '#1e1e1e',
            textAlign: 'center'
          }}>
            Monthly KYC Pass Rate Decline
          </h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart
              data={passRateData}
              margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e8e8f0" vertical={false} />
              <XAxis
                dataKey="week"
                tick={{ fontSize: 13, fill: '#666' }}
                axisLine={{ stroke: '#e0e0e0' }}
                label={{ value: 'Month (2017)', position: 'insideBottom', offset: -10, style: { fill: '#666', fontSize: 14 } }}
              />
              <YAxis
                domain={[50, 100]}
                tick={{ fontSize: 13, fill: '#666' }}
                axisLine={{ stroke: '#e0e0e0' }}
                label={{ value: 'Pass Rate (%)', angle: -90, position: 'insideLeft', style: { fill: '#666', fontSize: 14 } }}
              />
              <Tooltip
                contentStyle={{
                  background: 'rgba(255,255,255,0.95)',
                  border: '1px solid #e0e0e0',
                  borderRadius: '6px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.15)'
                }}
              />
              <Legend
                verticalAlign="top"
                height={36}
                iconType="line"
                wrapperStyle={{ fontSize: '13px' }}
              />
              {/* Target line at 85% */}
              <Line
                type="monotone"
                dataKey={() => 85}
                stroke="#3fb950"
                strokeWidth={2}
                strokeDasharray="5 5"
                name="Target (85%)"
                dot={false}
              />
              {/* Actual pass rate line */}
              <Line
                type="monotone"
                dataKey="passRate"
                stroke="#ef4444"
                strokeWidth={3}
                name="Pass Rate"
                dot={{
                  fill: '#ef4444',
                  strokeWidth: 2,
                  r: 6,
                  stroke: '#fff'
                }}
                activeDot={{ r: 8 }}
                label={{
                  position: 'top',
                  style: {
                    fontSize: 13,
                    fontWeight: '600',
                    fill: '#1e1e1e'
                  },
                  formatter: (value) => `${value.toFixed(1)}%`
                }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Pass Rate Health */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '300px 1fr',
          gap: '1.5rem',
          marginBottom: '1.5rem'
        }}>
          <div style={{
            background: 'rgba(255,255,255,0.95)',
            borderRadius: '8px',
            padding: '1.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem', fontWeight: '600' }}>
              Pass Rate Health
            </h3>
            <p style={{ margin: '0 0 1rem 0', fontSize: '0.85rem', color: '#666', lineHeight: '1.4' }}>
              The percentage of KYC attempts that successfully pass both document and face verification checks.
            </p>
          </div>

          <div style={{
            background: 'rgba(255,255,255,0.95)',
            borderRadius: '8px',
            padding: '1.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #e0e0e0' }}>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'left', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>PROJECT</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'right', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>LAST 8W</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'center', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>8W AVG</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'right', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>LAST 7 DAYS</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'right', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>DIFFERENCE</th>
                </tr>
              </thead>
              <tbody>
                {subCheckHealth.map((check, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid #f0f0f0' }}>
                    <td style={{ padding: '0.75rem', fontSize: '0.9rem' }}>
                      <div style={{ fontWeight: '500', color: '#1e1e1e' }}>{check.check}</div>
                      <div style={{ fontSize: '0.8rem', color: '#666', marginTop: '0.2rem' }}>{check.project}</div>
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right' }}>
                      <MiniBarChart bars={check.bars} />
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center', fontWeight: '600', fontSize: '0.95rem' }}>
                      {check.last8w}%
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right', fontWeight: '600', fontSize: '0.95rem' }}>
                      {check.last7d}%
                    </td>
                    <td style={{
                      padding: '0.75rem',
                      textAlign: 'right',
                      fontWeight: '600',
                      color: check.difference < 0 ? '#f55459' : check.difference > 0 ? '#3fb950' : '#666'
                    }}>
                      {check.difference > 0 ? '+' : ''}{check.difference}%
                      {check.difference < -10 ? ' ↓' : check.difference < 0 ? ' ↓' : check.difference > 0 ? ' ↑' : ''}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Key Transactions */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '300px 1fr',
          gap: '1.5rem',
          marginBottom: '1.5rem'
        }}>
          <div style={{
            background: 'rgba(255,255,255,0.95)',
            borderRadius: '8px',
            padding: '1.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem', fontWeight: '600' }}>
              Key Endpoints
            </h3>
            <p style={{ margin: '0 0 1rem 0', fontSize: '0.85rem', color: '#666', lineHeight: '1.4' }}>
              Success rates for critical KYC verification endpoints over time.
            </p>
          </div>

          <div style={{
            background: 'rgba(255,255,255,0.95)',
            borderRadius: '8px',
            padding: '1.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #e0e0e0' }}>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'left', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>⭐ KEY TRANSACTION</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'left', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>PROJECT</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'center', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>LAST 8W</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'center', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>LAST 7 DAYS</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'right', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>CHANGE</th>
                </tr>
              </thead>
              <tbody>
                {keyTransactions.map((tx, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid #f0f0f0' }}>
                    <td style={{ padding: '0.75rem', fontSize: '0.85rem', fontFamily: 'Monaco, monospace', color: '#0969da' }}>
                      {tx.transaction}
                    </td>
                    <td style={{ padding: '0.75rem' }}>
                      <span style={{
                        background: '#fef3c7',
                        color: '#92400e',
                        padding: '0.2rem 0.5rem',
                        borderRadius: '4px',
                        fontSize: '0.75rem',
                        fontWeight: '600'
                      }}>
                        {tx.project}
                      </span>
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      <MiniBarChart bars={tx.bars8w} />
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      <MiniBarChart bars={tx.bars7d} />
                    </td>
                    <td style={{
                      padding: '0.75rem',
                      textAlign: 'right',
                      fontWeight: '600',
                      fontSize: '0.9rem',
                      color: getChangeColor(tx.change)
                    }}>
                      {tx.change}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Metric Alerts Triggered */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '300px 1fr',
          gap: '1.5rem'
        }}>
          <div style={{
            background: 'rgba(255,255,255,0.95)',
            borderRadius: '8px',
            padding: '1.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem', fontWeight: '600' }}>
              Metric Alerts Triggered
            </h3>
            <p style={{ margin: '0 0 1rem 0', fontSize: '0.85rem', color: '#666', lineHeight: '1.4' }}>
              Alerts triggered from the monitoring rules your team configured.
            </p>
          </div>

          <div style={{
            background: 'rgba(255,255,255,0.95)',
            borderRadius: '8px',
            padding: '1.5rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            {/* Chart */}
            <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'flex-end' }}>
              <div style={{ fontSize: '0.8rem', color: '#666', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ width: '12px', height: '12px', background: '#4a5568', borderRadius: '2px' }} />
                Alerts Triggered
              </div>
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={alertsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
                <XAxis
                  dataKey="date"
                  tick={{ fontSize: 12, fill: '#666' }}
                  axisLine={{ stroke: '#e0e0e0' }}
                />
                <YAxis
                  tick={{ fontSize: 12, fill: '#666' }}
                  axisLine={{ stroke: '#e0e0e0' }}
                />
                <Tooltip />
                <Bar dataKey="alerts" fill="#4a5568" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>

            {/* Table */}
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '2rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #e0e0e0' }}>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'left', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>ALERT RULE</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'left', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>PROJECT</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'right', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>LAST 8W AVERAGE</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'right', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>THIS WEEK</th>
                  <th style={{ padding: '0.5rem 0.75rem', textAlign: 'right', fontSize: '0.85rem', fontWeight: '600', color: '#666' }}>DIFFERENCE</th>
                </tr>
              </thead>
              <tbody>
                {alertRules.map((rule, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid #f0f0f0' }}>
                    <td style={{ padding: '0.75rem', fontSize: '0.9rem', fontWeight: '500' }}>
                      {rule.rule}
                    </td>
                    <td style={{ padding: '0.75rem' }}>
                      <span style={{
                        background: '#fef3c7',
                        color: '#92400e',
                        padding: '0.2rem 0.5rem',
                        borderRadius: '4px',
                        fontSize: '0.75rem',
                        fontWeight: '600'
                      }}>
                        {rule.project}
                      </span>
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right', fontWeight: '600' }}>
                      {rule.last8wAvg}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right', fontWeight: '600' }}>
                      {rule.thisWeek}
                    </td>
                    <td style={{ padding: '0.75rem', textAlign: 'right', fontWeight: '600', color: '#f55459' }}>
                      {rule.difference}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

// Components
const NavItem = ({ icon, label, active }) => (
  <div style={{
    padding: '0.6rem 1rem',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    fontSize: '0.9rem',
    background: active ? '#2d2d2d' : 'transparent',
    color: active ? 'white' : '#888',
    borderLeft: active ? '3px solid #1fa9f4' : '3px solid transparent'
  }}>
    <span>{icon}</span>
    <span>{label}</span>
  </div>
);

const Tab = ({ label, active, onClick }) => (
  <div
    onClick={onClick}
    style={{
      padding: '0.75rem 0',
      cursor: 'pointer',
      fontSize: '0.95rem',
      fontWeight: active ? '600' : '400',
      color: active ? '#1e1e1e' : '#666',
      borderBottom: active ? '2px solid #1fa9f4' : '2px solid transparent',
      marginBottom: '-1px'
    }}
  >
    {label}
  </div>
);

const MiniBarChart = ({ bars }) => (
  <div style={{ display: 'flex', gap: '2px', height: '20px', alignItems: 'flex-end' }}>
    {bars.map((value, idx) => (
      <div
        key={idx}
        style={{
          width: '4px',
          height: value === 1 ? '100%' : '30%',
          background: value === 1 ? '#4a5568' : '#e0e0e0',
          borderRadius: '1px'
        }}
      />
    ))}
  </div>
);

export default KYCMonitoringDashboard;