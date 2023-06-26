import { Button, Flex, Grid, Group, LoadingOverlay, Modal, Stack, Text, Title } from '@mantine/core';
import React, { Dispatch, ReactElement, SetStateAction, useState } from 'react';
import { useDisclosure } from '@mantine/hooks';
import { useNavigate } from "react-router-dom";
import { Searchbar } from '../Components/Searchbar';

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

interface ItemProps {
  image: string;
  label: string;
  value: string;
  description: string;
}

function mapDataToItemProps(data: {
  id: string;
  name: string;
  logo_url: string;
}): ItemProps {
  return {
    image: data.logo_url,
    label: data.name,
    value: data.id,
    description: data.name,
  };
}

interface SearchAppProps {
  setAppData: Dispatch<SetStateAction<PolicyObject[]>>;
}

export default function SearchApp({ setAppData }: SearchAppProps): ReactElement<SearchAppProps> {
  const navigate = useNavigate();
  const [visible, { toggle }] = useDisclosure(false);
  const [appList, setAppList] = useState<string[]>([]);
  const [showModal, setShowModal] = useState(false);

  const handleSubmit = (): void => {
    console.log(appList);

    let list = { id: appList };

    toggle();

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
        navigate("./overview");
        console.log(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  const refresh = () => {
    setShowModal(false)
    toggle()

    fetch('http://localhost:8000/db_refresh', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        console.log(response);

        fetch('http://localhost:8000/get_db')
          .then((response) => response.json())
          .then((data) => {
            const convdata = JSON.parse(data).map(mapDataToItemProps);
            setAppList(convdata);
            console.log(convdata);
            toggle()
          })
          .catch((error) => {
            console.error('Error:', error);
            toggle()
          });
      })
      .catch((error) => {
        console.error('Error:', error);
        toggle()
      });
  };

  return (
    <>
      <Stack p={20}>
        <section>
          <Title>Check privacy policies by app name</Title>
          <Text>
            This page allows you to search for an app inside of our database by providing th app names you want to check. Our system will retrieve and analyze the privacy policies of the selected apps to provide you with valuable insights.
            <br/><br/>
            To get started, follow these steps:
            <br/>
            <ol>
              <li>Search for Apps.</li>
              <li>Click the "Check policies" button to initiate the process.</li>
            </ol>
            Our application will then collect the necessary data and present you with the results. We aim to help you make informed decisions about the apps you use based on their privacy policies.

            <br/><br/>
            <i>If you want to update the database, you can click on the "Refresh database" button. Attention: The refresh process might take some time!</i>
            <br/>
          
           
          </Text>
        </section>

        <section>
          <Grid>
            <Grid.Col span={10}>
              <LoadingOverlay visible={visible} overlayBlur={2} />
              <Searchbar setAppList={setAppList} />
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

        <section>
          <Button color="teal" variant="outline" onClick={() => setShowModal(true)}>
            Refresh database
          </Button>
        </section>
      </Stack>

      <Modal
        opened={showModal}
        onClose={() => setShowModal(false)}
        title="Refresh Warning"
        size="md"
    
      >
        
          <Text>
            Refreshing the database may take a long time. Are you sure you want to proceed?
          </Text>

   

          <Group mt="xl" position="center">
          <Button
            color="red"
            variant="filled"
            onClick={() => setShowModal(false)}
     
          >
            Cancel
          </Button>
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
