import { Button, Flex, Grid, Group, LoadingOverlay, Modal, Stack, Text, Title } from '@mantine/core';
import React, { Dispatch, ReactElement, SetStateAction, useState } from 'react';
import { useNavigate } from "react-router-dom";
import { Searchbar } from '../Components/Searchbar';

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

// Define interface for ItemProps used in search results
interface ItemProps {
  image: string;
  label: string;
  value: string;
  description: string;
}

// Function to map app data to ItemProps
function mapDataToItemProps(data: { id: string; name: string; logo_url: string }): ItemProps {
  return {
    image: data.logo_url,
    label: data.name,
    value: data.id,
    description: data.name,
  };
}

// Define props interface for the SearchApp component
interface SearchAppProps {
  setAppData: Dispatch<SetStateAction<PolicyObject[]>>;
}

// SearchApp component
export default function SearchApp({ setAppData }: SearchAppProps): ReactElement<SearchAppProps> {
  // Initialize the navigate function from react-router-dom to enable page navigation
  const navigate = useNavigate();

  // Initialize the loadingState and appList states using the useState hook from React
  const [loadingState, toggle] = useState(false);
  const [appList, setAppList] = useState<string[]>([]);

  // Initialize the showModal state using the useState hook from React to control the modal visibility
  const [showModal, setShowModal] = useState(false);

  // Function to handle form submission when the "Check policies" button is clicked
  const handleSubmit = (): void => {
    // Create a list object with the selected app names
    let list = { id: appList };
    // Show the loading overlay
    toggle(true);

    // Send a POST request to the backend API with the selected app names
    fetch('http://127.0.0.1:8000/id', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(list),
    })
      .then(response => response.json())
      .then(data => {
        // Once the data is retrieved, update the app data state with the new data
        setAppData(data);
        // Navigate to the "overview" page to display the results
        navigate("./overview");
      })
      .catch(error => {
        // Handle error if the request fails
        console.error('Error:', error);
      });
  };

  // Function to refresh the database
  const refresh = () => {
    // Close the modal
    setShowModal(false);
    // Show the loading overlay
    toggle(true);

    // Send a POST request to the backend API to refresh the database
    fetch('http://localhost:8000/db_refresh', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(() => {
        // After refreshing the database, fetch the updated app data from the API
        fetch('http://localhost:8000/get_db')
          .then((response) => response.json())
          .then((data) => {
            // Convert the data to ItemProps format using the mapDataToItemProps function and update the appList state
            const convdata = JSON.parse(data).map(mapDataToItemProps);
            setAppList(convdata);
          })
          .catch((error) => {
            // Handle error if fetching the data fails
            console.error('Error:', error);
          });
      })
      .catch((error) => {
        // Handle error if refreshing the database fails
        console.error('Error:', error);
      })
      .finally(() => {
        // Hide the loading overlay when the process is completed
        toggle(false);
      });
  };

  // Render the component
  return (
    <>
      <Stack p={20}>
        <section>
          {/* Title and description */}
          <Title>Check privacy policies by app name</Title>
          <Text>
            {/* Description of the page */}
            This page allows you to search for an app inside of our database by providing the app names you want to check.
            Our system will retrieve and analyze the privacy policies of the selected apps to provide you with valuable insights.
            <br/><br/>
            To get started, follow these steps:
            <br/>
            <ol>
              <li>Search for Apps.</li>
              <li>Click the "Check policies" button to initiate the process.</li>
            </ol>
            Our application will then collect the necessary data and present you with the results. We aim to help you make informed decisions about the apps you use based on their privacy policies.

            <br/><br/>
            {/* Note about refreshing the database */}
            <i>If you want to update the database, you can click on the "Refresh database" button. Attention: The refresh process might take some time!</i>
          </Text>
        </section>

        <section>
          <Grid>
            {/* Grid to display the search bar and "Check policies" button */}
            <Grid.Col span={10}>
              {/* Loading overlay to show loading state */}
              <LoadingOverlay visible={loadingState} overlayBlur={2} />
              {/* Searchbar component to search for apps */}
              <Searchbar setAppList={setAppList} />
            </Grid.Col>

            <Grid.Col span={2} display="flex">
              <Flex align="end">
                {/* Button to submit the search and check policies */}
                <Button color="dark" onClick={handleSubmit}>
                  Check policies
                </Button>
              </Flex>
            </Grid.Col>
          </Grid>
        </section>

        <section>
          {/* Button to refresh the database */}
          <Button color="teal" variant="outline" onClick={() => setShowModal(true)}>
            Refresh database
          </Button>
        </section>
      </Stack>

      {/* Modal to confirm the database refresh */}
      <Modal
        opened={showModal}
        onClose={() => setShowModal(false)}
        title="Refresh Warning"
        size="md"
      >
        <Text>
          {/* Warning message */}
          Refreshing the database may take a long time (about 10 minutes). Are you sure you want to proceed?
        </Text>

        {/* Group to align buttons */}
        <Group mt="xl" position="center">
          {/* Button to cancel the database refresh */}
          <Button
            color="red"
            variant="filled"
            onClick={() => setShowModal(false)}
          >
            Cancel
          </Button>
          {/* Button to proceed with the database refresh */}
          <Button
            color="dark"
            variant="filled"
            onClick={refresh}
          >
            Proceed
          </Button>
        </Group>
      </Modal>
    </>
  );
}
