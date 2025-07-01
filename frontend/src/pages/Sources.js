import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { sourcesService } from '../services/api';

const Sources = () => {
  const { isAuthenticated } = useAuth();
  const queryClient = useQueryClient();
  const [showAddForm, setShowAddForm] = useState(false);
  const [newSource, setNewSource] = useState({
    name: '',
    url: '',
    source_type: 'deep_web',
    keywords: '',
  });

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Query for sources
  const { data: sources, isLoading, error } = useQuery(
    'sources',
    () => sourcesService.getAll(),
    {
      refetchInterval: 30000,
    }
  );

  // Create source mutation
  const createMutation = useMutation(sourcesService.create, {
    onSuccess: () => {
      queryClient.invalidateQueries('sources');
      setShowAddForm(false);
      setNewSource({ name: '', url: '', source_type: 'deep_web', keywords: '' });
    },
  });

  // Delete source mutation
  const deleteMutation = useMutation(sourcesService.delete, {
    onSuccess: () => {
      queryClient.invalidateQueries('sources');
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    const keywords = newSource.keywords
      ? newSource.keywords.split(',').map(k => k.trim()).filter(k => k)
      : [];
    
    createMutation.mutate({
      ...newSource,
      keywords,
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'inactive': return 'bg-gray-100 text-gray-800';
      case 'error': return 'bg-red-100 text-red-800';
      case 'auth_failed': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'deep_web': return '🕳️';
      case 'telegram': return '💬';
      case 'forum': return '💭';
      case 'marketplace': return '🏪';
      default: return '🌐';
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Monitoring Sources</h1>
        <button
          onClick={() => setShowAddForm(true)}
          className="btn-primary"
        >
          Add Source
        </button>
      </div>

      {/* Add Source Form */}
      {showAddForm && (
        <div className="card">
          <div className="card-header">
            <h2 className="text-lg font-semibold text-gray-900">Add New Source</h2>
          </div>
          <div className="card-content">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Name</label>
                  <input
                    type="text"
                    required
                    value={newSource.name}
                    onChange={(e) => setNewSource({ ...newSource, name: e.target.value })}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder="e.g., Alpha Forum"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Type</label>
                  <select
                    value={newSource.source_type}
                    onChange={(e) => setNewSource({ ...newSource, source_type: e.target.value })}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="deep_web">Deep Web</option>
                    <option value="telegram">Telegram</option>
                    <option value="forum">Forum</option>
                    <option value="marketplace">Marketplace</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">URL</label>
                <input
                  type="url"
                  required
                  value={newSource.url}
                  onChange={(e) => setNewSource({ ...newSource, url: e.target.value })}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="https://example.onion or @telegram_channel"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Keywords (comma-separated)</label>
                <input
                  type="text"
                  value={newSource.keywords}
                  onChange={(e) => setNewSource({ ...newSource, keywords: e.target.value })}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="breach, leak, database, credentials"
                />
              </div>
              
              <div className="flex space-x-3">
                <button
                  type="submit"
                  disabled={createMutation.isLoading}
                  className="btn-primary disabled:opacity-50"
                >
                  {createMutation.isLoading ? 'Adding...' : 'Add Source'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowAddForm(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
              </div>
              
              {createMutation.error && (
                <div className="text-red-600 text-sm">
                  Error: {createMutation.error.response?.data?.detail || 'Failed to add source'}
                </div>
              )}
            </form>
          </div>
        </div>
      )}

      {/* Sources List */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-lg font-semibold text-gray-900">
            Active Sources ({sources?.data?.length || 0})
          </h2>
        </div>
        <div className="card-content">
          {error ? (
            <div className="text-center py-8 text-red-600">
              Error loading sources: {error.response?.data?.detail || error.message}
            </div>
          ) : sources?.data?.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <div className="text-4xl mb-2">📡</div>
              <p>No monitoring sources configured</p>
              <p className="text-sm">Add your first source to start monitoring</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Source</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Type</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Status</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Last Check</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {sources?.data?.map((source) => (
                    <tr key={source.id} className="border-b border-gray-100">
                      <td className="py-3 px-4">
                        <div>
                          <div className="font-medium text-gray-900">{source.name}</div>
                          <div className="text-sm text-gray-500 truncate max-w-xs">
                            {source.url}
                          </div>
                          {source.keywords && source.keywords.length > 0 && (
                            <div className="flex flex-wrap gap-1 mt-1">
                              {source.keywords.slice(0, 3).map((keyword, idx) => (
                                <span
                                  key={idx}
                                  className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
                                >
                                  {keyword}
                                </span>
                              ))}
                              {source.keywords.length > 3 && (
                                <span className="text-xs text-gray-500">
                                  +{source.keywords.length - 3} more
                                </span>
                              )}
                            </div>
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex items-center space-x-2">
                          <span className="text-lg">{getTypeIcon(source.source_type)}</span>
                          <span className="capitalize">{source.source_type.replace('_', ' ')}</span>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(source.status)}`}>
                          {source.status.replace('_', ' ')}
                        </span>
                        {source.error_count > 0 && (
                          <div className="text-xs text-red-600 mt-1">
                            {source.error_count} errors
                          </div>
                        )}
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">
                        {source.last_checked
                          ? new Date(source.last_checked).toLocaleString()
                          : 'Never'
                        }
                      </td>
                      <td className="py-3 px-4">
                        <button
                          onClick={() => deleteMutation.mutate(source.id)}
                          disabled={deleteMutation.isLoading}
                          className="text-red-600 hover:text-red-900 text-sm font-medium disabled:opacity-50"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Sources;