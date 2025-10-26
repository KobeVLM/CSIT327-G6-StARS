import { useState } from 'react';
import { Upload, Search, Award, ImageIcon, TrendingUp, Edit, X } from 'lucide-react';

interface DashboardProps {
  username: string;
  fullName: string;
  onNavigate: (page: string) => void;
  userStats: {
    posts: number;
    badges: number;
  };
}

const mockPosts = [
  { id: 1, title: 'Sunset Landscape', caption: 'A beautiful sunset over mountains', image: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200&h=150&fit=crop', username: 'artist1' },
  { id: 2, title: 'Abstract Colors', caption: 'Playing with vibrant colors', image: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=200&h=150&fit=crop', username: 'creator2' },
  { id: 3, title: 'Digital Portrait', caption: 'Character design practice', image: 'https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=200&h=150&fit=crop', username: 'painter3' },
  { id: 4, title: 'City Lights', caption: 'Urban photography edit', image: 'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=200&h=150&fit=crop', username: 'urbanart' },
];

const recentActivity = [
  { id: 1, action: 'received a like', item: 'Sunset Landscape', time: '2 hours ago' },
  { id: 2, action: 'earned badge', item: 'First Upload', time: '1 day ago' },
  { id: 3, action: 'got shared', item: 'Abstract Colors', time: '2 days ago' },
];

export function Dashboard({ username, fullName, onNavigate, userStats }: DashboardProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [showResults, setShowResults] = useState(false);

  const filteredResults = searchQuery.trim()
    ? mockPosts.filter(post => 
        post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        post.caption.toLowerCase().includes(searchQuery.toLowerCase()) ||
        post.username.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : [];

  return (
    <div className="p-8 max-w-6xl">
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.5rem' }}>
              Welcome back, {fullName}! 🎨
            </h1>
            <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
              Here's what's happening with your artwork today
            </p>
          </div>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setShowResults(true);
              }}
              onFocus={() => setShowResults(true)}
              className="w-full pl-10 pr-10 py-2.5 border border-input rounded-lg bg-white"
              style={{ fontSize: '0.875rem' }}
            />
            {searchQuery && (
              <button
                onClick={() => {
                  setSearchQuery('');
                  setShowResults(false);
                }}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Search Results */}
          {showResults && searchQuery && (
            <>
              <div 
                className="fixed inset-0 z-10" 
                onClick={() => setShowResults(false)}
              />
              <div className="absolute top-full mt-2 w-full bg-white rounded-lg shadow-lg border border-border max-h-96 overflow-y-auto z-20">
                {filteredResults.length > 0 ? (
                  <div className="p-2">
                    {filteredResults.map(post => (
                      <div
                        key={post.id}
                        className="flex items-center gap-3 p-3 hover:bg-secondary rounded-lg cursor-pointer transition-colors"
                        onClick={() => {
                          setShowResults(false);
                          onNavigate('browse');
                        }}
                      >
                        <img 
                          src={post.image} 
                          alt={post.title}
                          className="w-16 h-16 object-cover rounded"
                        />
                        <div className="flex-1 min-w-0">
                          <div style={{ fontSize: '0.875rem', fontWeight: '500', marginBottom: '0.25rem' }}>
                            {post.title}
                          </div>
                          <div style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                            {post.caption}
                          </div>
                          <div style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                            by @{post.username}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="p-8 text-center">
                    <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>No results found.</p>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-white rounded-lg p-6 border border-border">
          <div className="flex items-center justify-between mb-2">
            <div className="bg-primary/10 rounded-lg p-2">
              <ImageIcon className="w-5 h-5 text-primary" />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.25rem' }}>
            {userStats.posts}
          </div>
          <div style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>Posts Created</div>
        </div>

        <div className="bg-white rounded-lg p-6 border border-border">
          <div className="flex items-center justify-between mb-2">
            <div className="bg-yellow-500/10 rounded-lg p-2">
              <Award className="w-5 h-5 text-yellow-500" />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.25rem' }}>
            {userStats.badges}
          </div>
          <div style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>Badges Earned</div>
        </div>

        <div className="bg-white rounded-lg p-6 border border-border">
          <div className="flex items-center justify-between mb-2">
            <div className="bg-success/10 rounded-lg p-2">
              <TrendingUp className="w-5 h-5 text-success" />
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.25rem' }}>
            +12%
          </div>
          <div style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>Growth This Week</div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-white rounded-lg p-6 border border-border">
          <div className="bg-primary/10 rounded-lg p-3 inline-block mb-3">
            <Upload className="w-6 h-6 text-primary" />
          </div>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem' }}>
            Upload New Post
          </h3>
          <p style={{ fontSize: '0.875rem', color: '#7C8AA0', marginBottom: '1rem' }}>
            Share your latest artwork with the community
          </p>
          <button
            onClick={() => onNavigate('upload')}
            className="bg-primary text-white px-6 py-2.5 rounded hover:opacity-90 transition-opacity inline-flex items-center gap-2"
            style={{ fontSize: '0.875rem', fontWeight: '500' }}
          >
            <Upload className="w-4 h-4" />
            Upload Artwork
          </button>
        </div>

        <div className="bg-white rounded-lg p-6 border border-border">
          <div className="bg-secondary rounded-lg p-3 inline-block mb-3">
            <Edit className="w-6 h-6 text-primary" />
          </div>
          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem' }}>
            Edit Profile
          </h3>
          <p style={{ fontSize: '0.875rem', color: '#7C8AA0', marginBottom: '1rem' }}>
            Update your information and preferences
          </p>
          <button
            onClick={() => onNavigate('profile')}
            className="bg-secondary text-foreground px-6 py-2.5 rounded hover:bg-secondary/80 transition-colors"
            style={{ fontSize: '0.875rem', fontWeight: '500' }}
          >
            Go to Profile
          </button>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg p-6 border border-border">
        <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '1rem' }}>
          Recent Activity
        </h3>
        <div className="space-y-3">
          {recentActivity.map(activity => (
            <div key={activity.id} className="flex items-start gap-3 pb-3 border-b border-border last:border-0 last:pb-0">
              <div className="w-2 h-2 rounded-full bg-primary mt-2"></div>
              <div className="flex-1">
                <div style={{ fontSize: '0.875rem' }}>
                  Your post <span style={{ fontWeight: '500' }}>"{activity.item}"</span> {activity.action}
                </div>
                <div style={{ fontSize: '0.75rem', color: '#7C8AA0', marginTop: '0.25rem' }}>
                  {activity.time}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
