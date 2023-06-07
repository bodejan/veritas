import { Button, Flex, Grid, LoadingOverlay, Stack, Text, Title } from '@mantine/core';
import React, { Dispatch, ReactElement, SetStateAction, useState } from 'react'
import { useDisclosure } from '@mantine/hooks';
import { useNavigate } from "react-router-dom";
import { Searchbar } from '../Components/Searchbar';

interface Policy {
    [key: string]: number;
  }
  
  interface PolicyObject {
    id: string;
    name: string;
    image: string;
    policies: Policy;
  }
  
  interface SearchAppProps{
    setAppData: Dispatch<SetStateAction<PolicyObject[]>>,
  }



export default function SearchApp({setAppData}: SearchAppProps): ReactElement<SearchAppProps> {
  const navigate = useNavigate();

  const [visible, { toggle }] = useDisclosure(false);

  const [appList, setAppList] = useState<string[]>([]);

  const handleSubmit = (): void => {
    console.log(appList);

    let list = {id: appList}

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
            <Grid.Col span={10}>
            <LoadingOverlay visible={visible} overlayBlur={2} />
                <Searchbar setAppList={setAppList}/>
            </Grid.Col>

            <Grid.Col span={2} display="flex" >
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
  )
}
