import { useState } from 'react';
import { AlertTriangle, Ban, Trash2, CheckCircle } from 'lucide-react';

const reportedPosts = [
  {
    id: 1,
    title: 'Inappropriate Content',
    author: 'user123',
    reportedBy: 'moderator1',
    reason: 'Violates community guidelines',
    date: '2024-10-18',
    imageUrl: 'https://images.unsplash.com/photo-1579762715118-a6f1d4b934f1?w=200&h=150&fit=crop',
  },
  {
    id: 2,
    title: 'Spam Post',
    author: 'spammer456',
    reportedBy: 'moderator2',
    reason: 'Promotional spam content',
    date: '2024-10-19',
    imageUrl: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=200&h=150&fit=crop',
  },
];

const flaggedUsers = [
  {
    id: 1,
    username: 'violator789',
    email: 'violator@example.com',
    violations: 3,
    lastViolation: '2024-10-18',
    status: 'active',
  },
  {
    id: 2,
    username: 'reported_user',
    email: 'reported@example.com',
    violations: 1,
    lastViolation: '2024-10-17',
    status: 'active',
  },
];

export function Moderation() {
  const [actionStatus, setActionStatus] = useState<string | null>(null);

  const handleDeletePost = (postId: number) => {
    setActionStatus(`Post ${postId} has been deleted`);
    setTimeout(() => setActionStatus(null), 3000);
  };

  const handleSuspendUser = (userId: number) => {
    setActionStatus(`User ${userId} has been suspended`);
    setTimeout(() => setActionStatus(null), 3000);
  };

  const handleDismiss = () => {
    setActionStatus('Report has been dismissed');
    setTimeout(() => setActionStatus(null), 3000);
  };

  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.5rem' }}>
          Content Moderation
        </h1>
        <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
          Manage reported content and user violations
        </p>
      </div>

      {actionStatus && (
        <div className="bg-success/10 border border-success/20 rounded-lg px-4 py-3 mb-6 flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-success" />
          <p style={{ fontSize: '0.875rem', color: 'var(--success)' }}>{actionStatus}</p>
        </div>
      )}

      <div className="mb-8">
        <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '1rem' }}>
          Reported Posts
        </h2>
        
        <div className="space-y-4">
          {reportedPosts.map(post => (
            <div key={post.id} className="bg-white rounded-lg p-5 border border-destructive/20">
              <div className="flex gap-4">
                <img 
                  src={post.imageUrl} 
                  alt={post.title}
                  className="w-32 h-24 object-cover rounded"
                />
                
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.25rem' }}>
                        {post.title}
                      </h3>
                      <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
                        by {post.author}
                      </p>
                    </div>
                    <div className="flex items-center gap-1 px-2 py-1 bg-destructive/10 rounded">
                      <AlertTriangle className="w-4 h-4 text-destructive" />
                      <span style={{ fontSize: '0.75rem', color: 'var(--destructive)' }}>
                        Reported
                      </span>
                    </div>
                  </div>
                  
                  <div className="mb-3">
                    <p style={{ fontSize: '0.875rem', marginBottom: '0.25rem' }}>
                      <span style={{ fontWeight: '500' }}>Reason:</span> {post.reason}
                    </p>
                    <p style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                      Reported by {post.reportedBy} on {new Date(post.date).toLocaleDateString()}
                    </p>
                  </div>
                  
                  <div className="flex gap-3">
                    <button
                      onClick={() => handleDeletePost(post.id)}
                      className="bg-destructive text-white px-4 py-2 rounded hover:opacity-90 transition-opacity inline-flex items-center gap-2"
                      style={{ fontSize: '0.875rem' }}
                    >
                      <Trash2 className="w-4 h-4" />
                      Delete Post
                    </button>
                    <button
                      onClick={handleDismiss}
                      className="bg-white text-foreground border border-input px-4 py-2 rounded hover:bg-secondary transition-colors"
                      style={{ fontSize: '0.875rem' }}
                    >
                      Dismiss Report
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '1rem' }}>
          Flagged Users
        </h2>
        
        <div className="bg-white rounded-lg overflow-hidden">
          <table className="w-full">
            <thead className="bg-secondary/30">
              <tr>
                <th className="text-left px-4 py-3" style={{ fontSize: '0.875rem', fontWeight: '600' }}>
                  Username
                </th>
                <th className="text-left px-4 py-3" style={{ fontSize: '0.875rem', fontWeight: '600' }}>
                  Email
                </th>
                <th className="text-left px-4 py-3" style={{ fontSize: '0.875rem', fontWeight: '600' }}>
                  Violations
                </th>
                <th className="text-left px-4 py-3" style={{ fontSize: '0.875rem', fontWeight: '600' }}>
                  Last Violation
                </th>
                <th className="text-left px-4 py-3" style={{ fontSize: '0.875rem', fontWeight: '600' }}>
                  Status
                </th>
                <th className="text-left px-4 py-3" style={{ fontSize: '0.875rem', fontWeight: '600' }}>
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              {flaggedUsers.map(user => (
                <tr key={user.id} className="border-t border-border">
                  <td className="px-4 py-3" style={{ fontSize: '0.875rem' }}>
                    {user.username}
                  </td>
                  <td className="px-4 py-3" style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
                    {user.email}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center px-2 py-1 rounded ${
                      user.violations >= 3 ? 'bg-destructive/10 text-destructive' : 'bg-yellow-50 text-yellow-600'
                    }`} style={{ fontSize: '0.75rem', fontWeight: '500' }}>
                      {user.violations} violation{user.violations !== 1 ? 's' : ''}
                    </span>
                  </td>
                  <td className="px-4 py-3" style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
                    {new Date(user.lastViolation).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3">
                    <span className="inline-flex items-center px-2 py-1 rounded bg-green-50 text-green-600" style={{ fontSize: '0.75rem', fontWeight: '500' }}>
                      {user.status}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => handleSuspendUser(user.id)}
                      className="text-destructive hover:underline inline-flex items-center gap-1"
                      style={{ fontSize: '0.875rem' }}
                    >
                      <Ban className="w-4 h-4" />
                      Suspend
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
