import { Button, FileInput, Stack, Text, Textarea, Title, LoadingOverlay, Box } from '@mantine/core';
import { useForm } from '@mantine/form';
import React, { Dispatch, ReactElement, SetStateAction, useState } from 'react';
import { useDisclosure } from '@mantine/hooks';
import { useNavigate } from "react-router-dom";

type FormData = {
  category: string;
  numApps: number;
};

interface Policy {
  [key: string]: number;
}

interface PolicyObject {
  id: string;
  name: string;
  image: string;
  policies: Policy;
}

interface CheckListProps{
  setAppData: Dispatch<SetStateAction<PolicyObject[]>>,
}

export default function CheckList({setAppData}: CheckListProps): ReactElement<CheckListProps> {
  const navigate = useNavigate();

  const [visible, { toggle }] = useDisclosure(false);

  const [appList, setAppList] = useState<string[]>([]);

  
  const handleFileUpload = (file: File | null): void => {
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target?.result;
        if (typeof content === 'string') {
          const apps = content.split('\n');
          setAppList(apps);
        }
      };
      reader.readAsText(file);
    }
  };

  const handleSubmit = (): void => {
    console.log(appList);

    let list = {"id": appList}

    toggle()

        // Send the POST request
        fetch('http://127.0.0.1:8000/id', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(list),
        })
          .then(response => response.json())
          .then(data => {
            setAppData(data);
            //setTimeout(() => { navigate("./overview"); }, 7000);
            navigate("./overview")
            console.log(data)
          })
          .catch(error => {
            // Handle error if the request fails
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
        <LoadingOverlay visible={visible} overlayBlur={2} />

        <Stack>
        <section>
          <FileInput
            placeholder="Upload list of apps as CSV"
            label="Upload list"
            withAsterisk
            onChange={(files) => handleFileUpload(files)}
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
            onChange={(event) => setAppList(event.currentTarget.value.split('\n'))}
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
