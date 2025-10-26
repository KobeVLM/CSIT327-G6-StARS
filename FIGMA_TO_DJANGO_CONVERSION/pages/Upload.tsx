import { useState, useRef } from 'react';
import { Upload as UploadIcon, X, AlertCircle, CheckCircle, Loader2, Hash } from 'lucide-react';

interface UploadProps {
  onUploadComplete: () => void;
}

const filters = [
  { id: 'none', name: 'Original', filter: 'none' },
  { id: 'grayscale', name: 'Grayscale', filter: 'grayscale(100%)' },
  { id: 'sepia', name: 'Sepia', filter: 'sepia(100%)' },
  { id: 'brightness', name: 'Bright', filter: 'brightness(1.3)' },
  { id: 'contrast', name: 'Contrast', filter: 'contrast(1.3)' },
  { id: 'vintage', name: 'Vintage', filter: 'sepia(50%) contrast(1.2)' },
];

export function Upload({ onUploadComplete }: UploadProps) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    visibility: 'public',
  });
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [selectedFilter, setSelectedFilter] = useState('none');
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState('');
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!selectedFile) {
      setError('Please select an image file.');
      return;
    }

    if (!formData.title.trim()) {
      setError('Please enter a title.');
      return;
    }

    if (!formData.category) {
      setError('Please select a category.');
      return;
    }

    setUploading(true);
    setUploadProgress(0);

    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            onUploadComplete();
          }, 500);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type (only images)
    if (!file.type.startsWith('image/')) {
      setError('Unsupported file format. Please select an image file (PNG, JPG, GIF).');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size exceeds 10MB.');
      return;
    }

    setError('');
    setSelectedFile(file);
    
    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviewUrl(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleAddTag = () => {
    // Limit to 1 tag only
    if (tags.length >= 1) {
      setError('You can only add 1 tag. Remove the existing tag to add a new one.');
      return;
    }
    
    const trimmedTag = tagInput.trim();
    if (trimmedTag && !tags.includes(trimmedTag)) {
      if (trimmedTag.match(/^[a-zA-Z0-9_]+$/)) {
        setTags([...tags, trimmedTag]);
        setTagInput('');
      } else {
        setError('Invalid tag format. Use only letters, numbers, and underscores.');
      }
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleTagKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  const currentFilter = filters.find(f => f.id === selectedFilter);

  return (
    <div className="p-8 max-w-4xl">
      <div className="mb-6">
        <h1 style={{ fontSize: '1.75rem', fontWeight: '600', marginBottom: '0.5rem' }}>
          Upload Artwork
        </h1>
        <p style={{ fontSize: '0.875rem', color: '#7C8AA0' }}>
          Share your creative work with the community
        </p>
      </div>

      {error && (
        <div className="mb-6 p-3 bg-destructive/10 border border-destructive/20 rounded flex items-start gap-2">
          <AlertCircle className="w-4 h-4 text-destructive mt-0.5 flex-shrink-0" />
          <p style={{ fontSize: '0.875rem', color: 'var(--destructive)' }}>{error}</p>
        </div>
      )}

      {uploading && (
        <div className="mb-6 p-4 bg-primary/10 border border-primary/20 rounded">
          <div className="flex items-center gap-3 mb-2">
            <Loader2 className="w-5 h-5 text-primary animate-spin" />
            <span style={{ fontSize: '0.875rem', fontWeight: '500', color: 'var(--primary)' }}>
              Uploading... {uploadProgress}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-primary h-full rounded-full transition-all"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-white rounded-lg p-6">
          <label className="block mb-2" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
            Image Upload *
          </label>
          <div className="border-2 border-dashed border-border rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer">
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
              disabled={uploading}
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              {previewUrl ? (
                <div className="space-y-3">
                  <div className="relative inline-block">
                    <img 
                      src={previewUrl} 
                      alt="Preview" 
                      className="max-h-64 rounded"
                      style={{ filter: currentFilter?.filter }}
                    />
                  </div>
                  <div className="flex items-center justify-center gap-2">
                    <CheckCircle className="w-4 h-4 text-success" />
                    <span style={{ fontSize: '0.875rem', color: 'var(--success)' }}>
                      {selectedFile?.name}
                    </span>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.preventDefault();
                        setSelectedFile(null);
                        setPreviewUrl('');
                        setSelectedFilter('none');
                        if (fileInputRef.current) fileInputRef.current.value = '';
                      }}
                      className="text-muted-foreground hover:text-foreground"
                      disabled={uploading}
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <UploadIcon className="w-12 h-12 mx-auto mb-3 text-muted-foreground" />
                  <p style={{ fontSize: '0.875rem', color: '#7C8AA0', marginBottom: '0.25rem' }}>
                    Click to upload or drag and drop
                  </p>
                  <p style={{ fontSize: '0.75rem', color: '#7C8AA0' }}>
                    PNG, JPG, or GIF (max. 10MB)
                  </p>
                </>
              )}
            </label>
          </div>
        </div>

        {/* Filters */}
        {previewUrl && (
          <div className="bg-white rounded-lg p-6">
            <label className="block mb-3" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
              Image Filters
            </label>
            <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
              {filters.map(filter => (
                <button
                  key={filter.id}
                  type="button"
                  onClick={() => setSelectedFilter(filter.id)}
                  className={`relative border-2 rounded-lg overflow-hidden transition-all ${
                    selectedFilter === filter.id 
                      ? 'border-primary' 
                      : 'border-border hover:border-primary/50'
                  }`}
                  disabled={uploading}
                >
                  <div 
                    className="aspect-square bg-gradient-to-br from-gray-200 to-gray-300"
                    style={{ filter: filter.filter }}
                  />
                  <div className="p-2 text-center">
                    <span style={{ fontSize: '0.75rem' }}>{filter.name}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="bg-white rounded-lg p-6 space-y-5">
          <div>
            <label htmlFor="title" className="block mb-2" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
              Caption / Description *
            </label>
            <input
              id="title"
              type="text"
              value={formData.title}
              onChange={(e) => handleChange('title', e.target.value)}
              placeholder="Enter artwork caption"
              className="w-full px-3 py-2 border border-input rounded bg-white"
              style={{ fontSize: '0.875rem' }}
              required
              disabled={uploading}
            />
          </div>

          <div>
            <label htmlFor="description" className="block mb-2" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
              Description
            </label>
            <textarea
              id="description"
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              placeholder="Tell us more about your artwork..."
              rows={4}
              className="w-full px-3 py-2 border border-input rounded bg-white resize-none"
              style={{ fontSize: '0.875rem' }}
              disabled={uploading}
            />
          </div>

          <div>
            <label htmlFor="category" className="block mb-2" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
              Category Selection *
            </label>
            <select
              id="category"
              value={formData.category}
              onChange={(e) => handleChange('category', e.target.value)}
              className="w-full px-3 py-2 border border-input rounded bg-white"
              style={{ fontSize: '0.875rem' }}
              required
              disabled={uploading}
            >
              <option value="">Select a category</option>
              <option value="digital">Digital Painting</option>
              <option value="abstract">Abstract Art</option>
              <option value="illustration">Illustration</option>
              <option value="traditional">Traditional Art</option>
              <option value="character">Character Art</option>
              <option value="watercolor">Watercolor</option>
            </select>
          </div>

          {/* Tags */}
          <div>
            <label htmlFor="tags" className="block mb-2" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
              Tag (1 only)
            </label>
            <div className="flex gap-2 mb-2">
              <input
                id="tags"
                type="text"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={handleTagKeyDown}
                placeholder={tags.length >= 1 ? "Tag limit reached" : "Add a tag (e.g., portrait, digital, art)"}
                className="flex-1 px-3 py-2 border border-input rounded bg-white disabled:opacity-50 disabled:cursor-not-allowed"
                style={{ fontSize: '0.875rem' }}
                disabled={uploading || tags.length >= 1}
              />
              <button
                type="button"
                onClick={handleAddTag}
                className="bg-secondary text-foreground px-4 py-2 rounded hover:bg-secondary/80 transition-colors inline-flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                style={{ fontSize: '0.875rem', fontWeight: '500' }}
                disabled={uploading || tags.length >= 1}
              >
                <Hash className="w-4 h-4" />
                Add
              </button>
            </div>
            {tags.length >= 1 && (
              <p className="text-muted-foreground mb-2" style={{ fontSize: '0.75rem' }}>
                Maximum 1 tag allowed. Remove the existing tag to add a different one.
              </p>
            )}
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {tags.map(tag => (
                  <span
                    key={tag}
                    className="inline-flex items-center gap-1.5 bg-primary/10 text-primary px-3 py-1 rounded-full"
                    style={{ fontSize: '0.75rem', fontWeight: '500' }}
                  >
                    #{tag}
                    <button
                      type="button"
                      onClick={() => handleRemoveTag(tag)}
                      className="hover:text-primary/70"
                      disabled={uploading}
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          <div>
            <label className="block mb-2" style={{ fontSize: '0.875rem', fontWeight: '500' }}>
              Visibility
            </label>
            <div className="flex gap-4">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  name="visibility"
                  value="public"
                  checked={formData.visibility === 'public'}
                  onChange={(e) => handleChange('visibility', e.target.value)}
                  className="w-4 h-4 text-primary"
                  disabled={uploading}
                />
                <span style={{ fontSize: '0.875rem' }}>Public</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  name="visibility"
                  value="private"
                  checked={formData.visibility === 'private'}
                  onChange={(e) => handleChange('visibility', e.target.value)}
                  className="w-4 h-4 text-primary"
                  disabled={uploading}
                />
                <span style={{ fontSize: '0.875rem' }}>Private</span>
              </label>
            </div>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            type="submit"
            className="bg-primary text-white px-6 py-2.5 rounded hover:opacity-90 transition-opacity disabled:opacity-50"
            style={{ fontSize: '0.875rem', fontWeight: '500' }}
            disabled={uploading}
          >
            {uploading ? 'Uploading...' : 'Upload Artwork'}
          </button>
          <button
            type="button"
            onClick={() => window.history.back()}
            className="bg-white text-foreground border border-input px-6 py-2.5 rounded hover:bg-secondary transition-colors"
            style={{ fontSize: '0.875rem', fontWeight: '500' }}
            disabled={uploading}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
