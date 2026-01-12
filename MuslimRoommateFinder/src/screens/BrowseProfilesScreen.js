import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  TouchableOpacity,
  Image,
  RefreshControl,
  TextInput,
} from 'react-native';
import { profileAPI } from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function BrowseProfilesScreen({ navigation }) {
  const { profile } = useAuth();
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadProfiles();
  }, []);

  const loadProfiles = async () => {
    try {
      setLoading(true);
      const data = await profileAPI.getAllProfiles();
      // Filter out current user's profile
      const filtered = data.filter(p => p.id !== profile?.id);
      setProfiles(filtered);
    } catch (error) {
      console.error('Failed to load profiles:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredProfiles = profiles.filter(p => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    return (
      p.name?.toLowerCase().includes(query) ||
      p.city?.toLowerCase().includes(query) ||
      p.state?.toLowerCase().includes(query)
    );
  });

  const renderProfile = ({ item }) => (
    <TouchableOpacity
      style={styles.profileCard}
      onPress={() => navigation.navigate('ProfileDetail', { profileId: item.id })}
    >
      {item.profile_photo && (
        <Image source={{ uri: item.profile_photo }} style={styles.photo} />
      )}
      <View style={styles.profileInfo}>
        <Text style={styles.name}>{item.name}</Text>
        <Text style={styles.location}>
          {item.city}, {item.state}
        </Text>
        {item.age && <Text style={styles.age}>{item.age} years old</Text>}
        
        <View style={styles.badges}>
          {item.only_eats_zabihah && (
            <Text style={styles.badge}>🍖 Zabihah</Text>
          )}
          {item.prayer_friendly && (
            <Text style={styles.badge}>🕌 Prayer</Text>
          )}
          {item.guests_allowed && (
            <Text style={styles.badge}>👥 Guests</Text>
          )}
          {item.is_looking_for_room && (
            <Text style={styles.badge}>🔍 Looking</Text>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchInput}
          placeholder="Search by name or location..."
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
      </View>

      <FlatList
        data={filteredProfiles}
        renderItem={renderProfile}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
          <RefreshControl refreshing={loading} onRefresh={loadProfiles} />
        }
        ListEmptyComponent={
          <View style={styles.emptyState}>
            <Text style={styles.emptyText}>No profiles found</Text>
          </View>
        }
        contentContainerStyle={styles.listContent}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  searchContainer: {
    padding: 15,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  searchInput: {
    backgroundColor: '#f5f5f5',
    padding: 12,
    borderRadius: 8,
    fontSize: 16,
  },
  listContent: {
    padding: 15,
  },
  profileCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    flexDirection: 'row',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  photo: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginRight: 15,
  },
  profileInfo: {
    flex: 1,
    justifyContent: 'center',
  },
  name: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  location: {
    fontSize: 14,
    color: '#666',
    marginBottom: 3,
  },
  age: {
    fontSize: 14,
    color: '#999',
    marginBottom: 8,
  },
  badges: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  badge: {
    backgroundColor: '#e9ecef',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    marginRight: 5,
    marginTop: 3,
    fontSize: 11,
  },
  emptyState: {
    padding: 40,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: '#999',
  },
});

