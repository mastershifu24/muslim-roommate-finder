import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  RefreshControl,
  Image,
  Linking,
} from 'react-native';
import { useAuth } from '../context/AuthContext';
import { profileAPI } from '../api/client';

export default function HomeScreen({ navigation }) {
  const { profile, user } = useAuth();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (profile) {
      loadMatches();
    }
  }, [profile]);

  // Helper to normalize boolean values (API might return strings)
  const normalizeBooleans = (profile) => ({
    ...profile,
    only_eats_zabihah: Boolean(profile.only_eats_zabihah),
    prayer_friendly: Boolean(profile.prayer_friendly),
    guests_allowed: Boolean(profile.guests_allowed),
    is_looking_for_room: Boolean(profile.is_looking_for_room),
  });

  const loadMatches = async () => {
    try {
      setLoading(true);
      const profiles = await profileAPI.getAllProfiles();
      
      // Normalize booleans and calculate compatibility scores
      const profilesWithScores = profiles
        .filter(p => p.id !== profile?.id)
        .map(p => normalizeBooleans(p))
        .map(p => ({
          ...p,
          score: calculateCompatibility(p),
        }))
        .sort((a, b) => b.score - a.score)
        .slice(0, 10); // Top 10 matches
      
      setMatches(profilesWithScores);
    } catch (error) {
      console.error('Failed to load matches:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateCompatibility = (otherProfile) => {
    if (!profile) return 0;
    
    // Ensure both profiles have normalized booleans for comparison
    const normalizedProfile = {
      only_eats_zabihah: Boolean(profile.only_eats_zabihah),
      prayer_friendly: Boolean(profile.prayer_friendly),
      guests_allowed: Boolean(profile.guests_allowed),
    };
    const normalizedOther = {
      only_eats_zabihah: Boolean(otherProfile.only_eats_zabihah),
      prayer_friendly: Boolean(otherProfile.prayer_friendly),
      guests_allowed: Boolean(otherProfile.guests_allowed),
    };
    
    let score = 0;
    
    // Religious practices (40 points)
    if (normalizedProfile.only_eats_zabihah === normalizedOther.only_eats_zabihah) score += 20;
    if (normalizedProfile.prayer_friendly === normalizedOther.prayer_friendly) score += 20;
    
    // Location (30 points)
    if (profile.city && otherProfile.city) {
      if (profile.city.toLowerCase() === otherProfile.city.toLowerCase()) {
        score += 30;
      } else if (profile.state && otherProfile.state) {
        if (profile.state.toLowerCase() === otherProfile.state.toLowerCase()) {
          score += 15;
        }
      }
    }
    
    // Age proximity (20 points)
    if (profile.age && otherProfile.age) {
      const ageDiff = Math.abs(profile.age - otherProfile.age);
      if (ageDiff <= 3) score += 20;
      else if (ageDiff <= 5) score += 15;
      else if (ageDiff <= 10) score += 10;
      else if (ageDiff <= 15) score += 5;
    }
    
    // Guest policy (10 points)
    if (normalizedProfile.guests_allowed === normalizedOther.guests_allowed) score += 10;
    
    return Math.min(score, 100);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#28a745';
    if (score >= 60) return '#ffc107';
    return '#6c757d';
  };

  const openWhatsApp = (number) => {
    if (number) {
      const cleanNumber = number.replace(/[^\d+]/g, '');
      Linking.openURL(`https://wa.me/${cleanNumber}`);
    }
  };

  if (!profile) {
    return (
      <View style={styles.container}>
        <View style={styles.centerContent}>
          <Text style={styles.title}>Complete Your Profile</Text>
          <Text style={styles.subtitle}>
            Create your profile to start finding compatible roommates
          </Text>
          <TouchableOpacity
            style={styles.button}
            onPress={() => navigation.navigate('MyProfile')}
          >
            <Text style={styles.buttonText}>Create Profile</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={loading} onRefresh={loadMatches} />
      }
    >
      <View style={styles.header}>
        <Text style={styles.greeting}>As-salamu alaykum, {user?.first_name || user?.username}!</Text>
        <Text style={styles.subtitle}>Your top matches based on compatibility</Text>
      </View>

      {matches.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyText}>No matches found yet</Text>
          <Text style={styles.emptySubtext}>
            More profiles will appear as people join!
          </Text>
        </View>
      ) : (
        <View style={styles.matchesList}>
          {matches.map((match) => (
            <TouchableOpacity
              key={match.id}
              style={styles.matchCard}
              onPress={() => navigation.navigate('ProfileDetail', { profileId: match.id })}
            >
              <View style={styles.matchHeader}>
                {match.profile_photo && (
                  <Image
                    source={{ uri: match.profile_photo }}
                    style={styles.matchPhoto}
                  />
                )}
                <View style={styles.matchInfo}>
                  <Text style={styles.matchName}>{match.name}</Text>
                  <Text style={styles.matchLocation}>
                    {match.city}, {match.state}
                  </Text>
                  {match.age && (
                    <Text style={styles.matchAge}>{match.age} years old</Text>
                  )}
                </View>
                <View
                  style={[
                    styles.scorebadge,
                    { backgroundColor: getScoreColor(match.score) },
                  ]}
                >
                  <Text style={styles.scoreText}>{match.score}%</Text>
                </View>
              </View>

              <View style={styles.matchDetails}>
                {match.only_eats_zabihah && (
                  <Text style={styles.badge}>🍖 Zabihah Only</Text>
                )}
                {match.prayer_friendly && (
                  <Text style={styles.badge}>🕌 Prayer Friendly</Text>
                )}
                {match.guests_allowed && (
                  <Text style={styles.badge}>👥 Guests OK</Text>
                )}
              </View>

              {match.whatsapp_number && (
                <TouchableOpacity
                  style={styles.whatsappButton}
                  onPress={() => openWhatsApp(match.whatsapp_number)}
                >
                  <Text style={styles.whatsappText}>💬 Message on WhatsApp</Text>
                </TouchableOpacity>
              )}
            </TouchableOpacity>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centerContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  header: {
    backgroundColor: '#28a745',
    padding: 20,
    paddingTop: 40,
  },
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 5,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#28a745',
    marginBottom: 10,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#fff',
  },
  emptyState: {
    padding: 40,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#666',
    marginBottom: 10,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
  },
  matchesList: {
    padding: 15,
  },
  matchCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  matchHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  matchPhoto: {
    width: 60,
    height: 60,
    borderRadius: 30,
    marginRight: 15,
  },
  matchInfo: {
    flex: 1,
  },
  matchName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  matchLocation: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  matchAge: {
    fontSize: 14,
    color: '#999',
    marginTop: 2,
  },
  scoreBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  scoreText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  matchDetails: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 10,
  },
  badge: {
    backgroundColor: '#e9ecef',
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 15,
    marginRight: 8,
    marginTop: 5,
    fontSize: 12,
  },
  whatsappButton: {
    backgroundColor: '#25D366',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 5,
  },
  whatsappText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 14,
  },
  button: {
    backgroundColor: '#28a745',
    padding: 15,
    borderRadius: 8,
    marginTop: 20,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

