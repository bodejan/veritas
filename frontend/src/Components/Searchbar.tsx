import React, { Dispatch, SetStateAction, forwardRef, useState } from 'react';
import { MultiSelect, Avatar, Group, Text } from '@mantine/core';


const data = [
    {
    image: "https://play-lh.googleusercontent.com/bYtqbOcTYOlgc6gqZ2rwb8lptHuwlNE75zYJu6Bn076-hTmvd96HH-6v7S0YUAAJXoJN=w20",
    label: "WhatsApp",
    value: "com.whatsapp",
    description: "Messaging and calling app"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/instagram-new.png",
    label: "Instagram",
    value: "com.instagram.android",
    description: "Social media platform for sharing photos and videos"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/facebook-new.png",
    label: "Facebook",
    value: "com.facebook.katana",
    description: "Social networking platform"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/twitter.png",
    label: "Twitter",
    value: "Twitter",
    description: "Social networking and microblogging platform"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/youtube.png",
    label: "YouTube",
    value: "YouTube",
    description: "Video sharing platform"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/spotify.png",
    label: "Spotify",
    value: "Spotify",
    description: "Music streaming service"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/netflix.png",
    label: "Netflix",
    value: "com.netflix.mediaclient",
    description: "Streaming platform for movies and TV shows"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/uber-app.png",
    label: "Uber",
    value: "com.ubercab",
    description: "Ride-sharing and transportation service"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/google-maps-new.png",
    label: "Google Maps",
    value: "Google Maps",
    description: "Mapping and navigation app"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/gmail.png",
    label: "Gmail",
    value: "Gmail",
    description: "Email service by Google"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/slack.png",
    label: "Slack",
    value: "Slack",
    description: "Team collaboration and communication app"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/tiktok.png",
    label: "TikTok",
    value: "TikTok",
    description: "Short-form video app"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/zoom.png",
    label: "Zoom",
    value: "Zoom",
    description: "Video conferencing app"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/pinterest.png",
    label: "Pinterest",
    value: "Pinterest",
    description: "Visual discovery and bookmarking tool"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/shazam.png",
    label: "Shazam",
    value: "Shazam",
    description: "Music identification app"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/whatsapp.png",
    label: "WhatsApp",
    value: "WhatsApp",
    description: "Messaging and calling app"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/viber.png",
    label: "Viber",
    value: "Viber",
    description: "Messaging and calling app"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/telegram-app.png",
    label: "Telegram",
    value: "Telegram",
    description: "Messaging app with a focus on privacy"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/linkedin.png",
    label: "LinkedIn",
    value: "LinkedIn",
    description: "Professional networking platform"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/whatsapp.png",
    label: "WhatsApp",
    value: "WhatsApp",
    description: "Messaging and calling app"
    },
    {
    image: "https://img.icons8.com/clouds/256/000000/viber.png",
    label: "Viber",
    value: "Viber",
    description: "Messaging and calling app"
    }
    ];



interface ItemProps {
  image: string;
  label: string;
  description: string;
}

interface SearchbarProps{
  setAppList: Dispatch<SetStateAction<string[]>>,
}

const SelectItem = forwardRef<HTMLDivElement, ItemProps>(
  ({ image, label, description, ...others }: ItemProps, ref) => (
    <div ref={ref} {...others}>
      <Group>
        <Avatar src={image} />

        <div>
          <Text>{label}</Text>
          <Text size="xs" color="dimmed">
            {description}
          </Text>
        </div>
      </Group>
    </div>
  )
);

export function Searchbar({setAppList}: SearchbarProps) {


  return (
    <MultiSelect
      label="Search for Apps"
      placeholder="Select apps you want to analyse"
      itemComponent={SelectItem}
      onChange={(values) => setAppList(values)}
      data={data}
      searchable
      nothingFound="Nobody here"
      dropdownPosition="bottom" 
      maxDropdownHeight={300}
      limit={10}
      filter={(value, selected, item) =>
        !selected &&
        (item.label?.toLowerCase().includes(value.toLowerCase().trim()) ||
          item.description.toLowerCase().includes(value.toLowerCase().trim()))
      }
    />
  );
}
