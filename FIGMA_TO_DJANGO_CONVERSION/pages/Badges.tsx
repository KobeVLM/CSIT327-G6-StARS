import { Award, Star, Trophy, Target } from 'lucide-react';

const earnedBadges = [
  {
    id: 1,
    name: 'First Upload',
    description: 'Uploaded your first artwork',
    icon: Award,
    dateEarned: '2024-03-15',
    color: 'text-blue-500',
    bgColor: 'bg-blue-50',
  },
  {
    id: 2,
    name: 'Rising Star',
    description: 'Reached 100 total likes',
    icon: Star,
    dateEarned: '2024-04-02',
    color: 'text-yellow-500',
    bgColor: 'bg-yellow-50',
  },
  {
    id: 3,
    name: 'Dedicated Artist',
    description: 'Posted 10 artworks',
    icon: Target,
    dateEarned: '2024-05-10',
    color: 'text-green-500',
    bgColor: 'bg-green-50',
  },
];

const availableBadges = [
  {
    id: 4,
    name: 'Master Creator',
    description: 'Upload 50 artworks',
    icon: Trophy,
    levelRequired: 10,
    color: 'text-gray-400',
    bgColor: 'bg-gray-50',
  },
  {
    id: 5,
    name: 'Community Favorite',
    description: 'Reach 1000 total likes',
    icon: Award,
    levelRequired: 15,
    color: 'text-gray-400',
    bgColor: 'bg-gray-50',
  },
];

export function Badges() {
  const currentLevel = 3;
  const currentXP = 450;
  const nextLevelXP = 500;
  const xpProgress = (currentXP / nextLevelXP) * 100;

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.5rem' }}>
          Badges & Rewards
        </h1>
        <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
          Track your achievements and progress
        </p>
      </div>

      <div className="bg-white rounded-lg p-6 mb-6">
        <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '1rem' }}>
          Your Progress
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="bg-secondary/30 rounded-lg p-4 text-center">
            <div style={{ fontSize: '2rem', fontWeight: '600', color: 'var(--primary)', marginBottom: '0.25rem' }}>
              {currentLevel}
            </div>
            <div style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>Current Level</div>
          </div>
          
          <div className="bg-secondary/30 rounded-lg p-4 text-center">
            <div style={{ fontSize: '2rem', fontWeight: '600', color: 'var(--primary)', marginBottom: '0.25rem' }}>
              {currentXP}
            </div>
            <div style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>Total Experience</div>
          </div>
          
          <div className="bg-secondary/30 rounded-lg p-4 text-center">
            <div style={{ fontSize: '2rem', fontWeight: '600', color: 'var(--primary)', marginBottom: '0.25rem' }}>
              {earnedBadges.length}
            </div>
            <div style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>Badges Earned</div>
          </div>
        </div>

        <div>
          <div className="flex justify-between mb-2">
            <span style={{ fontSize: '0.875rem', fontWeight: '500' }}>
              Level {currentLevel} Progress
            </span>
            <span style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
              {currentXP} / {nextLevelXP} XP
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div 
              className="bg-primary h-full rounded-full transition-all"
              style={{ width: `${xpProgress}%` }}
            />
          </div>
        </div>
      </div>

      <div className="mb-6">
        <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.5rem' }}>
          Earned Badges
        </h2>
        <p style={{ fontSize: '0.875rem', color: '#7C8AA0', marginBottom: '1rem' }}>
          Congratulations on your achievements!
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {earnedBadges.map(badge => {
            const Icon = badge.icon;
            return (
              <div key={badge.id} className="bg-white rounded-lg p-5 border-2 border-primary/20">
                <div className="flex items-start gap-4">
                  <div className={`${badge.bgColor} rounded-lg p-3`}>
                    <Icon className={`w-6 h-6 ${badge.color}`} />
                  </div>
                  <div className="flex-1">
                    <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.25rem' }}>
                      {badge.name}
                    </h3>
                    <p style={{ fontSize: '0.75rem', color: '#7C8AA0', marginBottom: '0.5rem' }}>
                      {badge.description}
                    </p>
                    <p style={{ fontSize: '0.75rem', color: 'var(--primary)' }}>
                      Earned {new Date(badge.dateEarned).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div>
        <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.5rem' }}>
          Available Badges
        </h2>
        <p style={{ fontSize: '0.875rem', color: '#7C8AA0', marginBottom: '1rem' }}>
          Keep creating to unlock these badges
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {availableBadges.map(badge => {
            const Icon = badge.icon;
            return (
              <div key={badge.id} className="bg-white rounded-lg p-5 border border-border opacity-60">
                <div className="flex items-start gap-4">
                  <div className={`${badge.bgColor} rounded-lg p-3`}>
                    <Icon className={`w-6 h-6 ${badge.color}`} />
                  </div>
                  <div className="flex-1">
                    <h3 style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.25rem' }}>
                      {badge.name}
                    </h3>
                    <p style={{ fontSize: '0.75rem', color: '#7C8AA0', marginBottom: '0.5rem' }}>
                      {badge.description}
                    </p>
                    <p style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                      Required: Level {badge.levelRequired}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
