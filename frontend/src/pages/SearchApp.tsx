import { Button, Flex, Grid, LoadingOverlay, Stack, Text, Title } from '@mantine/core'; // Importing components from @mantine/core library
import React, { Dispatch, ReactElement, SetStateAction, useState } from 'react'; // Importing React-related dependencies
import { useDisclosure } from '@mantine/hooks'; // Importing a hook from @mantine/hooks library
import { useNavigate } from "react-router-dom"; // Importing a hook from react-router-dom library
import { Searchbar } from '../Components/Searchbar'; // Importing the Searchbar component

interface Policy {
  [key: string]: number;
}

interface PolicyObject {
  id: string;
  name: string;
  logo_url: string;
  policy: string;
  scores: Policy;
  status: string;
}



interface SearchAppProps {
  setAppData: Dispatch<SetStateAction<PolicyObject[]>>;
}

export default function SearchApp({ setAppData }: SearchAppProps): ReactElement<SearchAppProps> {
  const navigate = useNavigate(); // Initializing the useNavigate hook for programmatic navigation

  const [visible, { toggle }] = useDisclosure(false); // Initializing the useDisclosure hook to manage the visibility of a loading overlay

  const [appList, setAppList] = useState<string[]>([]); // Initializing state for the list of apps

  const handleSubmit = (): void => {
    console.log(appList);

    let list = { id: appList }; // Creating a list object with appList as its "id" property

    toggle(); // Toggling the loading overlay

    // Sending a POST request to a specified URL with the list object
    fetch('http://127.0.0.1:8000/id', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(list),
    })
      .then(response => response.json())
      .then(data => {
        setAppData(data); // Updating the app data state with the received data
        navigate("./overview"); // Navigating to the "./overview" route
        console.log(data);
      })
      .catch(error => {
        // Handling error if the request fails
        console.error('Error:', error);
      });
  };

  return (
    <>
      <Stack p={20}>
        <section>
          <Title>Check privacy policies by app category</Title>
          <Text>
            This page allows you to select an app category and specify the number of apps you want to check. Our system will retrieve and analyze the privacy policies of the selected apps to provide you with valuable insights.
            <br/><br/>
            To get started, follow these steps:
            <br/>
            <ol>
              <li>Choose an app category from the provided options.</li>
              <li>Enter the number of apps you would like to check within that category.</li>
              <li>Click the "Submit" button to initiate the process.</li>
            </ol>
          
            Our application will then collect the necessary data and present you with the results. We aim to help you make informed decisions about the apps you use based on their privacy policies.
          </Text>
        </section>

        <section>
          <Grid>
            <Grid.Col span={10}>
              <LoadingOverlay visible={visible} overlayBlur={2} /> {/* Rendering the loading overlay */}
              <Searchbar setAppList={setAppList} /> {/* Rendering the Searchbar component */}
            </Grid.Col>

            <Grid.Col span={2} display="flex">
              <Flex align="end">
                <Button color="dark" onClick={handleSubmit}>
                  Check policies
                </Button>
              </Flex>
            </Grid.Col>
          </Grid>
        </section>
      </Stack>
    </>
  );
}
