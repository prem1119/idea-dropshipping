import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Plus, Megaphone, TrendingUp } from 'lucide-react'
import './Ads.css'

function Ads() {
  const [campaigns, setCampaigns] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCampaigns()
  }, [])

  const fetchCampaigns = async () => {
    try {
      const response = await axios.get('/api/v1/ads/campaigns')
      setCampaigns(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching campaigns:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="ads-loading">Loading campaigns...</div>
  }

  return (
    <div className="ads">
      <div className="ads-header">
        <div>
          <h1>Ad Campaigns</h1>
          <p>Manage TikTok and Facebook ad campaigns</p>
        </div>
        <button className="create-campaign-btn">
          <Plus size={20} />
          Create Campaign
        </button>
      </div>

      <div className="campaigns-grid">
        {campaigns.length === 0 ? (
          <div className="empty-campaigns">
            <Megaphone size={64} />
            <h2>No campaigns yet</h2>
            <p>Create your first ad campaign to start driving traffic</p>
            <button className="create-campaign-btn-primary">
              <Plus size={20} />
              Create Campaign
            </button>
          </div>
        ) : (
          campaigns.map((campaign) => (
            <div key={campaign.id} className="campaign-card">
              <div className="campaign-header">
                <div className="campaign-platform">
                  <span className={`platform-badge platform-${campaign.platform}`}>
                    {campaign.platform}
                  </span>
                </div>
                <span className={`campaign-status status-${campaign.status}`}>
                  {campaign.status}
                </span>
              </div>
              <h3>{campaign.name}</h3>
              <div className="campaign-metrics">
                <div className="metric">
                  <span>Budget</span>
                  <strong>${campaign.budget.toFixed(2)}</strong>
                </div>
                {campaign.daily_budget && (
                  <div className="metric">
                    <span>Daily Budget</span>
                    <strong>${campaign.daily_budget.toFixed(2)}</strong>
                  </div>
                )}
              </div>
              {campaign.creative_caption && (
                <p className="campaign-caption">{campaign.creative_caption}</p>
              )}
              <div className="campaign-actions">
                <button className="action-btn">View Details</button>
                <button className="action-btn">Edit</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Ads

