import { Button, FileInput, Stack, Text, Textarea, Title, LoadingOverlay, Box } from '@mantine/core'; // Importing components from @mantine/core library
import { useForm } from '@mantine/form'; // Importing a hook from @mantine/form library
import React, { Dispatch, ReactElement, SetStateAction, useState } from 'react'; // Importing React-related dependencies
import { useDisclosure } from '@mantine/hooks'; // Importing a hook from @mantine/hooks library
import { useNavigate } from "react-router-dom"; // Importing a hook from react-router-dom library


// Define types for the policy and policy object
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

// Define props for the CheckList component
interface CheckListProps {
  setAppData: Dispatch<SetStateAction<PolicyObject[]>>;
}

export default function CheckList({ setAppData }: CheckListProps): ReactElement<CheckListProps> {
  const navigate = useNavigate(); // Initializing the useNavigate hook for programmatic navigation

  const [visible, { toggle }] = useDisclosure(false); // Initializing the useDisclosure hook to manage the visibility of a loading overlay

  const [appList, setAppList] = useState<string[]>([]); // Initializing state for the list of apps

  // Handle file upload and parse the app names
  const handleFileUpload = (file: File | null): void => {
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target?.result;
        if (typeof content === 'string') {
          const apps = content.split('\n'); // Splitting the file content by newline to get individual app names
          setAppList(apps); // Updating the appList state with the parsed app names
        }
      };
      reader.readAsText(file); // Reading the file as text
    }
  };

  // Handle form submission
  const handleSubmit = (): void => {
    console.log(appList);

    let list = {"id": appList} // Creating a list object with appList as its "id" property

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
          <Title>Check privacy policies by app list</Title>
          <Text>
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor
            invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et
            accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata
            sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur
            sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna
            aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea
            rebum.
          </Text>
        </section>

        <Box pos="relative">
          <LoadingOverlay visible={visible} overlayBlur={2} /> {/* Rendering the loading overlay */}

          <Stack>
            <section>
              <FileInput
                placeholder="Upload list of apps as CSV"
                label="Upload list"
                withAsterisk
                onChange={(files) => handleFileUpload(files)} // Handling file upload and parsing the app names
              />
            </section>

            <Title order={5}>Alternatively, you can insert a list with the package names of the apps</Title>

            <section>
              <Textarea
                placeholder="List of apps"
                label="List of apps"
                withAsterisk
                autosize
                minRows={6}
                onChange={(event) => setAppList(event.currentTarget.value.split('\n'))} // Handling manual input of app names
              />
            </section>

            <section>
              <Button color="dark" onClick={handleSubmit}>
                Check policies
              </Button>
            </section>
          </Stack>
        </Box>
      </Stack>
    </>
  );
}
