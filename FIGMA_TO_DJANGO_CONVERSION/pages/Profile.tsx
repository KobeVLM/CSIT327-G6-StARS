import { useState } from 'react';
import { Star, Award, Calendar, Heart, Share2, Edit, X } from 'lucide-react';

interface ProfileProps {
  username: string;
  fullName: string;
  level: number;
  xp: number;
}

const userArtworks = [
  {
    id: 1,
    title: 'My Latest Work',
    likes: 45,
    shares: 12,
    imageUrl: 'https://images.unsplash.com/photo-1579762715118-a6f1d4b934f1?w=400&h=300&fit=crop',
  },
  {
    id: 2,
    title: 'Abstract Study',
    likes: 67,
    shares: 23,
    imageUrl: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400&h=300&fit=crop',
  },
  {
    id: 3,
    title: 'Digital Portrait',
    likes: 89,
    shares: 34,
    imageUrl: 'https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=400&h=300&fit=crop',
  },
];

export function Profile({ username, fullName, level, xp }: ProfileProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [profileData, setProfileData] = useState({
    bio: 'Passionate digital artist exploring colors and creativity. Always learning, always creating.',
    email: username,
  });

  const [editData, setEditData] = useState(profileData);

  const handleSave = () => {
    setProfileData(editData);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditData(profileData);
    setIsEditing(false);
  };

  return (
    <div className="p-8 max-w-7xl">
      {/* Profile Header - Two Column Layout */}
      <div className="bg-white rounded-lg p-6 mb-6">
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-start gap-4 flex-1">
            <div className="w-24 h-24 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
              <span className="text-primary" style={{ fontSize: '2rem', fontWeight: '600' }}>
                {fullName.charAt(0).toUpperCase()}
              </span>
            </div>
            
            <div className="flex-1">
              <h1 style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                {fullName}
              </h1>
              <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
                @{username.split('@')[0]}
              </p>
            </div>
          </div>

          {/* Edit/Save/Cancel Buttons */}
          <div className="flex gap-2">
            {!isEditing ? (
              <button
                onClick={() => setIsEditing(true)}
                className="bg-primary text-white px-4 py-2 rounded hover:opacity-90 transition-opacity inline-flex items-center gap-2"
                style={{ fontSize: '0.875rem', fontWeight: '500' }}
              >
                <Edit className="w-4 h-4" />
                Edit Profile
              </button>
            ) : (
              <>
                <button
                  onClick={handleSave}
                  className="bg-success text-white w-9 h-9 rounded hover:opacity-90 transition-opacity inline-flex items-center justify-center"
                  title="Save changes"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </button>
                <button
                  onClick={handleCancel}
                  className="bg-destructive text-white w-9 h-9 rounded hover:opacity-90 transition-opacity inline-flex items-center justify-center"
                  title="Cancel"
                >
                  <X className="w-5 h-5" />
                </button>
              </>
            )}
          </div>
        </div>

        {/* Bio - Editable inline */}
        <div className="mb-6">
          {isEditing ? (
            <textarea
              value={editData.bio}
              onChange={(e) => setEditData({ ...editData, bio: e.target.value })}
              rows={3}
              className="w-full px-3 py-2 border border-primary rounded bg-white resize-none"
              style={{ fontSize: '0.875rem', lineHeight: '1.6' }}
              placeholder="Write your bio..."
            />
          ) : (
            <p style={{ fontSize: '0.875rem', color: '#2C3E50', lineHeight: '1.6' }}>
              {profileData.bio}
            </p>
          )}
        </div>
        
        {/* Level, XP, and Joined Date */}
        <div className="space-y-3 mb-6" style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
          <div className="flex items-center gap-2">
            <Star className="w-4 h-4 flex-shrink-0 text-yellow-500" />
            <span>Level {level}</span>
          </div>
          <div className="flex items-center gap-2">
            <Award className="w-4 h-4 flex-shrink-0 text-primary" />
            <span>{xp} XP</span>
          </div>
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 flex-shrink-0" />
            <span>Joined March 2024</span>
          </div>
        </div>

        {/* Stats */}
        <div className="flex gap-6 pb-6 border-b border-border" style={{ fontSize: '0.875rem' }}>
          <div>
            <span style={{ fontWeight: '600', marginRight: '0.25rem' }}>12</span>
            <span style={{ color: '#7C8AA0' }}>Artworks</span>
          </div>
          <div>
            <span style={{ fontWeight: '600', marginRight: '0.25rem' }}>456</span>
            <span style={{ color: '#7C8AA0' }}>Total Likes</span>
          </div>
          <div>
            <span style={{ fontWeight: '600', marginRight: '0.25rem' }}>89</span>
            <span style={{ color: '#7C8AA0' }}>Total Shares</span>
          </div>
        </div>

        {/* Account Details */}
        <div className="mt-6">
          <div style={{ fontSize: '0.75rem', color: '#7C8AA0', marginBottom: '0.5rem' }}>
            Account Details
          </div>
          <div style={{ fontSize: '0.875rem' }}>
            <span style={{ fontWeight: '500' }}>Email:</span> {profileData.email}
          </div>
        </div>
      </div>

      {/* Artworks Grid */}
      <div className="mb-4">
        <h2 style={{ fontSize: '1.25rem', fontWeight: '600' }}>My Artworks</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {userArtworks.map(artwork => (
          <div key={artwork.id} className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div className="aspect-[4/3] bg-gray-100 overflow-hidden">
              <img 
                src={artwork.imageUrl} 
                alt={artwork.title}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="p-4">
              <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.75rem' }}>
                {artwork.title}
              </h3>
              <div className="flex items-center gap-4" style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                <div className="flex items-center gap-1">
                  <Heart className="w-4 h-4" />
                  <span>{artwork.likes}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Share2 className="w-4 h-4" />
                  <span>{artwork.shares}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
