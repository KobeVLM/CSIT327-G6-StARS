import { useState } from 'react';
import { Heart, Share2, Eye, Sparkles } from 'lucide-react';

const mockArtworks = [
  {
    id: 1,
    title: 'Sunset Dreams',
    artist: 'sarah_art',
    artistName: 'Sarah Johnson',
    profilePic: '',
    caption: 'A beautiful sunset over the mountains',
    category: 'Digital Painting',
    filter: 'Sepia',
    tags: ['landscape', 'sunset', 'nature'],
    likes: 234,
    shares: 45,
    views: 1203,
    imageUrl: 'https://images.unsplash.com/photo-1579762715118-a6f1d4b934f1?w=400&h=300&fit=crop',
    filterStyle: 'sepia(50%) contrast(1.2)',
  },
  {
    id: 2,
    title: 'Abstract Emotions',
    artist: 'mike_creates',
    artistName: 'Mike Chen',
    profilePic: '',
    caption: 'Exploring color and form',
    category: 'Abstract Art',
    filter: 'Original',
    tags: ['abstract', 'colorful', 'modern'],
    likes: 189,
    shares: 32,
    views: 890,
    imageUrl: 'https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400&h=300&fit=crop',
    filterStyle: 'none',
  },
  {
    id: 3,
    title: 'Urban Sketches',
    artist: 'artby_emma',
    artistName: 'Emma Wilson',
    profilePic: '',
    caption: 'City life illustrations',
    category: 'Illustration',
    filter: 'Bright',
    tags: ['urban', 'sketch', 'city'],
    likes: 312,
    shares: 67,
    views: 1567,
    imageUrl: 'https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=400&h=300&fit=crop',
    filterStyle: 'brightness(1.3)',
  },
  {
    id: 4,
    title: 'Nature Study',
    artist: 'john_painter',
    artistName: 'John Smith',
    profilePic: '',
    caption: 'Traditional painting of flora',
    category: 'Traditional Art',
    filter: 'Grayscale',
    tags: ['nature', 'painting', 'botanical'],
    likes: 456,
    shares: 89,
    views: 2145,
    imageUrl: 'https://images.unsplash.com/photo-1547891654-e66ed7ebb968?w=400&h=300&fit=crop',
    filterStyle: 'grayscale(100%)',
  },
  {
    id: 5,
    title: 'Character Design',
    artist: 'lisa_design',
    artistName: 'Lisa Anderson',
    profilePic: '',
    caption: 'Original character concept',
    category: 'Character Art',
    filter: 'Contrast',
    tags: ['character', 'design', 'digital'],
    likes: 523,
    shares: 102,
    views: 2890,
    imageUrl: 'https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=400&h=300&fit=crop',
    filterStyle: 'contrast(1.3)',
  },
  {
    id: 6,
    title: 'Watercolor Flow',
    artist: 'tom_artist',
    artistName: 'Tom Davis',
    profilePic: '',
    caption: 'Fluid watercolor techniques',
    category: 'Watercolor',
    filter: 'Vintage',
    tags: ['watercolor', 'fluid', 'art'],
    likes: 278,
    shares: 54,
    views: 1432,
    imageUrl: 'https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400&h=300&fit=crop',
    filterStyle: 'sepia(50%) contrast(1.2)',
  },
];

export function Browse() {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [likedPosts, setLikedPosts] = useState<number[]>([]);
  const categories = ['All', 'Digital Painting', 'Abstract Art', 'Illustration', 'Traditional Art', 'Character Art', 'Watercolor'];

  const filteredArtworks = selectedCategory === 'All' 
    ? mockArtworks 
    : mockArtworks.filter(art => art.category === selectedCategory);

  const toggleLike = (id: number) => {
    if (likedPosts.includes(id)) {
      setLikedPosts(likedPosts.filter(postId => postId !== id));
    } else {
      setLikedPosts([...likedPosts, id]);
    }
  };

  return (
    <div className="p-8 max-w-7xl">
      <div className="mb-6">
        <h1 style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.5rem' }}>
          Browse Artworks
        </h1>
        <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
          Discover amazing creations from student artists
        </p>
      </div>

      <div className="mb-6 flex flex-wrap gap-2">
        {categories.map(category => (
          <button
            key={category}
            onClick={() => setSelectedCategory(category)}
            className={`px-4 py-2 rounded-lg transition-colors ${
              selectedCategory === category
                ? 'bg-primary text-white'
                : 'bg-white text-foreground hover:bg-secondary'
            }`}
            style={{ fontSize: '0.875rem' }}
          >
            {category}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredArtworks.map(artwork => (
          <div key={artwork.id} className="bg-white rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            {/* Image with Filter */}
            <div className="aspect-[4/3] bg-gray-100 overflow-hidden relative">
              <img 
                src={artwork.imageUrl} 
                alt={artwork.title}
                className="w-full h-full object-cover"
                style={{ filter: artwork.filterStyle }}
              />
              {artwork.filter !== 'Original' && (
                <div className="absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded flex items-center gap-1">
                  <Sparkles className="w-3 h-3" />
                  <span style={{ fontSize: '0.75rem' }}>{artwork.filter}</span>
                </div>
              )}
            </div>

            <div className="p-4">
              {/* User Info */}
              <div className="flex items-center gap-2 mb-3">
                <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                  <span className="text-primary" style={{ fontSize: '0.75rem', fontWeight: '600' }}>
                    {artwork.artistName.charAt(0)}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <div style={{ fontSize: '0.875rem', fontWeight: '500' }}>
                    {artwork.artistName}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                    @{artwork.artist}
                  </div>
                </div>
              </div>

              {/* Title and Caption */}
              <h3 style={{ fontSize: '1.125rem', fontWeight: '600', marginBottom: '0.5rem' }}>
                {artwork.title}
              </h3>
              <p style={{ fontSize: '0.875rem', color: '#7C8AA0', marginBottom: '0.75rem' }}>
                {artwork.caption}
              </p>

              {/* Tags */}
              {artwork.tags && artwork.tags.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mb-3">
                  {artwork.tags.map(tag => (
                    <button
                      key={tag}
                      className="bg-primary/10 text-primary px-2 py-0.5 rounded-full hover:bg-primary/20 transition-colors"
                      style={{ fontSize: '0.75rem', fontWeight: '500' }}
                    >
                      #{tag}
                    </button>
                  ))}
                </div>
              )}

              {/* Engagement Stats */}
              <div className="flex items-center justify-between pt-3 border-t border-border">
                <div className="flex items-center gap-4" style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                  <button
                    onClick={() => toggleLike(artwork.id)}
                    className="flex items-center gap-1 hover:text-primary transition-colors"
                  >
                    <Heart 
                      className={`w-4 h-4 ${likedPosts.includes(artwork.id) ? 'fill-primary text-primary' : ''}`}
                    />
                    <span>{artwork.likes + (likedPosts.includes(artwork.id) ? 1 : 0)}</span>
                  </button>
                  <div className="flex items-center gap-1">
                    <Share2 className="w-4 h-4" />
                    <span>{artwork.shares}</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Eye className="w-4 h-4" />
                    <span>{artwork.views}</span>
                  </div>
                </div>
                <span style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                  {artwork.category}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredArtworks.length === 0 && (
        <div className="text-center py-12">
          <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
            No artworks found in this category.
          </p>
        </div>
      )}
    </div>
  );
}
