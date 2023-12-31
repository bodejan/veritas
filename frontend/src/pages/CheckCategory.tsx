import { Button, Grid, LoadingOverlay, NativeSelect, NumberInput, Stack, Text, Title } from '@mantine/core'
import { useForm } from '@mantine/form';
import React, { Dispatch, ReactElement, SetStateAction } from 'react';
import { useDisclosure } from '@mantine/hooks';
import { useNavigate } from "react-router-dom";

// Define interface for form data
interface FormData {
  category: string;
  numApps: number;
}

// Define interface for the policy scores
interface Policy {
  [key: string]: number;
}

// Define interface for the app object
interface PolicyObject {
  id: string;
  name: string;
  logo_url: string;
  policy: string;
  scores: Policy;
  status: string;
}

// Define props interface for the CheckCategory component
interface CheckCategoryProps {
  setAppData: Dispatch<SetStateAction<PolicyObject[]>>;
}

// CheckCategory component
export default function CheckCategory({ setAppData }: CheckCategoryProps): ReactElement<CheckCategoryProps> {
  // Initialize form state and create form using the useForm hook from Mantine
  const form = useForm<FormData>({
    initialValues: {
      category: '',
      numApps: 1,
    },
  });

  // Initialize the navigate function from react-router-dom to enable page navigation
  const navigate = useNavigate();

  // Initialize the visible state and toggle function using the useDisclosure hook from Mantine
  const [visible, { toggle }] = useDisclosure(false);

  // Extract errors and input props from the form state
  const { errors, getInputProps } = form;

// App categories from Androidrank
  const categories = JSON.parse(JSON.stringify({
    "Select category": "",
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



  // Function to handle form submission
  function handleSubmit(): void {
    // Check if the form has a valid category and the number of apps is greater than or equal to 1
    if (form.values.category && form.values.numApps >= 1) {
      // Create a categoryObject with the selected category and number of apps
      var categoryObject = { category: form.values.category, number: form.values.numApps };

      // Log the categoryObject
      console.log(categoryObject);

      // Toggle the loading overlay to show loading state
      toggle();

      // Send a POST request to the backend API to retrieve data based on the selected category and number of apps
      fetch('http://127.0.0.1:8000/category', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(categoryObject),
      })
        .then(response => response.json())
        .then(data => {
          // Once the data is retrieved, update the app data state with the new data
          setAppData(data);
          // Navigate to the "overview" page to display the results
          navigate("./overview");
          // Log the received data
          console.log(data);
        })
        .catch(error => {
          // Handle error if the request fails
          console.error('Error:', error);
        });
    }
  }
  return (
    <>
      <Stack p={20}>
      <section>
          <Title>Check privacy policies by app category</Title>
          <Text>
          This page allows you to select an app category and specify the number of apps you want to check. Our system will retrieve and analyze the privacy policies of the selected apps to provide you with valuable insights.
          <br/>  <br/>
          To get started, follow these steps:
          <br/>
          <ol>
            <li> Choose an app category from the provided options.</li>
            <li>Enter the number of apps you would like to check within that category.</li>
            <li>Click the "Submit" button to initiate the process.</li>
          </ol>
         
          Our application will then collect the necessary data and present you with the results. We aim to help you make informed decisions about the apps you use based on their privacy policies.
          </Text>
        </section>

        <section>
          <Grid>
          <LoadingOverlay visible={visible} overlayBlur={2} />
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
