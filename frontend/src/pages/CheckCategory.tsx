import { Button, Grid, Input, NativeSelect, NumberInput, Stack, Text, Title } from '@mantine/core'
import { useForm } from '@mantine/form';
import React, { ReactElement } from 'react';

type FormData = {
  category: string;
  numApps: number;
};

type CategoryProps = {};

export default function CheckCategory(props: CategoryProps): ReactElement<CategoryProps> {
  const form = useForm<FormData>({
    initialValues: {
      category: '',
      numApps: 1,
    },

  });

  const { errors, getInputProps } = form;


  const categories = JSON.parse(JSON.stringify({
    "All": "",
    "Paid": "?price=paid",
    "Free": "?price=free",
    "Art And Design": "?category=ART_AND_DESIGN",
    "Auto And Vehicles": "?category=AUTO_AND_VEHICLES",
    "Beauty": "?category=BEAUTY",
    "Books And Reference": "?category=BOOKS_AND_REFERENCE",
    "Business": "?category=BUSINESS",
    "Comics": "?category=COMICS",
    "Communication": "?category=COMMUNICATION",
    "Dating": "?category=DATING",
    "Education": "?category=EDUCATION",
    "Entertainment": "?category=ENTERTAINMENT",
    "Events": "?category=EVENTS",
    "Finance": "?category=FINANCE",
    "Food And Drink": "?category=FOOD_AND_DRINK",
    "Health And Fitness": "?category=HEALTH_AND_FITNESS",
    "House And Home": "?category=HOUSE_AND_HOME",
    "Libraries And Demo": "?category=LIBRARIES_AND_DEMO",
    "Lifestyle": "?category=LIFESTYLE",
    "Maps And Navigation": "?category=MAPS_AND_NAVIGATION",
    "Medical": "?category=MEDICAL",
    "Music And Audio": "?category=MUSIC_AND_AUDIO",
    "News And Magazines": "?category=NEWS_AND_MAGAZINES",
    "Parenting": "?category=PARENTING",
    "Personalization": "?category=PERSONALIZATION",
    "Photography": "?category=PHOTOGRAPHY",
    "Productivity": "?category=PRODUCTIVITY",
    "Shopping": "?category=SHOPPING",
    "Social": "?category=SOCIAL",
    "Sports": "?category=SPORTS",
    "Tools": "?category=TOOLS",
    "Transportation": "?category=TRANSPORTATION",
    "Travel And Local": "?category=TRAVEL_AND_LOCAL",
    "Video Players": "?category=VIDEO_PLAYERS",
    "Weather": "?category=WEATHER",
    "Game Action": "?category=GAME_ACTION",
    "Game Adventure": "?category=GAME_ADVENTURE",
    "Game Arcade": "?category=GAME_ARCADE",
    "Game Board": "?category=GAME_BOARD",
    "Game Card": "?category=GAME_CARD",
    "Game Casino": "?category=GAME_CASINO",
    "Game Casual": "?category=GAME_CASUAL",
    "Game Educational": "?category=GAME_EDUCATIONAL",
    "Game Family": "?category=GAME_FAMILY",
    "Game Music": "?category=GAME_MUSIC",
    "Game Puzzle": "?category=GAME_PUZZLE",
    "Game Racing": "?category=GAME_RACING",
    "Game Role Playing": "?category=GAME_ROLE_PLAYING",
    "Game Simulation": "?category=GAME_SIMULATION",
    "Game Sports": "?category=GAME_SPORTS",
    "Game Strategy": "?category=GAME_STRATEGY",
    "Game Trivia": "?category=GAME_TRIVIA",
    "Game Word": "?category=GAME_WORD"
}))

  const handleSubmit = () => {
    if (form.values.category && form.values.numApps >= 1) {

      var categoryObject = {category : form.values.category, number: form.values.numApps}

      console.log(categoryObject)
    }
  };

  return (
    <>
      <Stack p={20}>
        <section>
          <Title>Check privacy policies by app category</Title>
          <Text>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. </Text>
        </section>

        <section>
          <Grid>
            <Grid.Col xs={12} lg={6}>
              <NativeSelect
                {...getInputProps('category')}
                data={Object.keys(categories)}
                label="Select category"
                description="Select a category for apps you want to check"
                withAsterisk
                required
              />
              {errors.category && <div>{errors.category}</div>}
            </Grid.Col>
            <Grid.Col xs={6} lg={4}>
              <NumberInput
                {...getInputProps('numApps')}
                label="Amount of Apps"
                description="How many apps do you want to analyze?"
                placeholder="1"
                min={1}
                withAsterisk
                required
              />
              {errors.numApps && <div>{errors.numApps}</div>}
            </Grid.Col>
            <Grid.Col xs={6} lg={2} display="flex" sx={{ alignItems: 'end' }}>
              <Button color="dark" onClick={handleSubmit}>
                Check policies
              </Button>
            </Grid.Col>
          </Grid>
        </section>
      </Stack>
    </>
  );
}
