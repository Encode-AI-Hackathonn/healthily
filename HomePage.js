

import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Animated, Text, Image } from 'react-native';

export default function MyComponent() {
  const rotationValue = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.loop(
      Animated.timing(rotationValue, {
        toValue: 1,
        duration: 6000, ///check this!!!
        useNativeDriver: true,
      }),
      { iterations: -1 }
    ).start();
  }, []);

  const spin = rotationValue.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  return (
    <View style={styles.container}>
      <View style={styles.topTextContainer}>
        <CurvedText text = "Welcome to CareConnect" radius={190} angle={105} style={styles.topText} />
      </View>
      <Animated.View style = {[styles.koiFish, { transform: [{ rotate: spin }] }]}>
        <Image source = {require('./assets/123.png')} style={styles.image} />
      </Animated.View>
      <Text style={styles.bottomText}> Health is Wealth </Text>
    </View>
  );
}

const CurvedText = ({ text, radius, angle, style }) => {
  const characters = text.split('');
  const step = angle / (characters.length - 1);
  const rotate = angle / 2;

  return (
    <View style = {[styles.container, { width: radius * 2, height: radius }]}>
      {characters.map((char, index) => (
        <Text
          key = {index}
          style = {[
            styles.text,
            {
              transform: [
                { translateY: radius },
                { rotate: `${index * step - rotate}deg` },
                { translateY: -radius },
              ],
            },
            style,
          ]}
        >
          {char}
        </Text>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white ',
    justifyContent: 'center',
    alignItems: 'center',
  },
  topTextContainer: {
    position: 'absolute',
    top: 40,
    width: '100%',
    alignItems: 'center',
    overflow: 'hidden',
  },
  topText: {
    fontSize: 45,
    color: 'black',
    fontWeight: 'bold',
  },
  koiFish: {
    width: 300,
    height: 300,
    borderRadius: 190,
    backgroundColor: 'cream',
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    width: 170,
    height: 200,
    borderRadius: 110,
  },
  bottomText: {
    fontSize: 40,
    color: 'black',
    fontWeight: 'bold',
    marginTop: 20,
  },
  text: {
    position: 'absolute',
  },
});


