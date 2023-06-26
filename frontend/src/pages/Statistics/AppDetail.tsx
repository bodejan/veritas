import React, { useState } from 'react';
import { Box, Button, Checkbox, Flex, Grid, Modal, Progress, RingProgress, ScrollArea, Stack, Text, Title, createStyles } from '@mantine/core';
import { CircleCheck, CircleX } from 'tabler-icons-react';
import { useDisclosure } from '@mantine/hooks';

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

interface OverviewProps {
  currentApp: PolicyObject;
}

const useStyles = createStyles((theme) => ({
  scollbox: {
    padding: 20,
    background: theme.colors.gray[1],
    borderRadius: 8,
  },
}));

export default function AppDetail({ currentApp }: OverviewProps) {
  const { classes, theme } = useStyles();

  const [opened, { open, close }] = useDisclosure(false);

  const [selectedHeaders, setSelectedHeaders] = useState<string[]>(['id', 'name', 'logo_url', ...Object.keys(currentApp.scores), 'status', 'policy']);


  const calculateScoreAverage = (scores: Policy): number => {
    const scoreValues = Object.values(scores);
    const sum = scoreValues.reduce((acc, score) => acc + score, 0);
    const average = sum / scoreValues.length;

    return average;
  };



  const handleExport = () => {
    const headers = ['id', 'name', 'logo_url', ...Object.keys(currentApp.scores), 'status'];
    const data = [headers, [currentApp.id, currentApp.name, currentApp.logo_url, ...Object.values(currentApp.scores), currentApp.status]];
    const csvData = data.map((row) => row.join(';')).join('\n');


    const link = document.createElement('a');
    link.href = `data:text/csv;charset=utf-8,${encodeURIComponent(csvData)}`;
    link.download = `${currentApp.name}_data.csv`;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  function handleHeaderToggle(header: string) {
    setSelectedHeaders((prevSelectedHeaders) => {
      if (prevSelectedHeaders.includes(header)) {
        return prevSelectedHeaders.filter((selectedHeader) => selectedHeader !== header);
      } else {
        return [...prevSelectedHeaders, header];
      }
    });
  }

  
  function downloadCSV() {
    const csvData = convertToCSV([currentApp]);
    const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.setAttribute('href', URL.createObjectURL(blob));
    link.setAttribute('download', 'appData.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
  

  function convertToCSV(data: PolicyObject[]): string {
    const csvRows = [];
  
    const headers = ['id', 'name', 'logo_url', ...Object.keys(currentApp.scores), 'status', 'policy'];

    // Add headers
    csvRows.push(selectedHeaders.join(';'));
  
    // Add data rows
    for (const row of data) {
      const values = [
        row.id,
        row.name,
        row.logo_url,
        ...Object.values(row.scores),
        row.status,
        row.policy.replace(/\n|\r/g, '').replaceAll(';', '|'),
      ].map((value) => String(value)); // Cast the value to string
  
      // Filter selected values based on selected headers
      const filteredValues = values.filter((_, index) => selectedHeaders.includes(headers[index]));
  
      csvRows.push(filteredValues.join(';'));
    }
  
    return csvRows.join('\n');
  }

  return (
    <>
      <Stack p={20}>
        <section>
          <Title>Check privacy policy of {currentApp.name}</Title>
          <Text>
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore
            et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
            Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit
            amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam
            erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
          </Text>
        </section>

        <Grid>
          <Grid.Col span={9}></Grid.Col>
          <Grid.Col span={3} sx={{ justifyContent: 'end', display: 'flex' }}>
            <Button color="dark" onClick={() => open()}>
              Export data
            </Button>
          </Grid.Col>
        </Grid>

        <Modal
          opened={opened} 
          onClose={close}
         
          title="Select Headers"
        >
          <Flex     
            gap="md"
            justify="flex-start"
            align="flex-start"
            direction="column"
            wrap="wrap">
            
  
            {['id', 'name', 'logo_url', ...Object.keys(currentApp.scores), 'status', 'policy'].map((header) => (
    
             <Checkbox
                key={header}
                label={header}
                checked={selectedHeaders.includes(header)}
                onChange={() => handleHeaderToggle(header)}
              >
               
              </Checkbox>
            
            ))}
          </Flex>
          <Button color="teal" mt="md" onClick={() => downloadCSV()}>
            Export
          </Button>
        </Modal>

        <section>
          <Grid>
            <Grid.Col xs={12} lg={5}>
              <Flex justify="center">
                <RingProgress
                  sections={[{ value: calculateScoreAverage(currentApp.scores) * 100, color: theme.colors.teal[7] }]}
                  size={280}
                  thickness={17}
                  roundCaps
                  label={
                    <Text color={theme.colors.teal[7]} weight={700} align="center" size="40px">
                      {calculateScoreAverage(currentApp.scores).toFixed(2)}
                    </Text>
                  }
                />
              </Flex>

              <Box className={classes.scollbox}>
                <Grid p={10}>
                  <Grid.Col span={6} display="grid" sx={{ alignContent: 'center', justifyContent: 'center' }}>
                    <Title order={6}>Category</Title>
                  </Grid.Col>
                  <Grid.Col span={6} display="grid" sx={{ alignContent: 'center', justifyContent: 'center' }}>
                    <Title order={6}>Result</Title>
                  </Grid.Col>
                </Grid>

                <Grid p={10}>
                  {Object.keys(currentApp.scores).map((value) => (
                    <>
                      <Grid.Col span={6} display="grid">
                        <Text>{value}</Text>
                      </Grid.Col>
                      <Grid.Col span={6} display="grid" sx={{ alignContent: 'center', justifyContent: 'center' }}>
                        {currentApp.scores[value] ? (
                          <CircleCheck color={theme.colors.green[6]} />
                        ) : (
                          <CircleX color={theme.colors.red[6]} />
                        )}
                      </Grid.Col>
                    </>
                  ))}
                </Grid>
              </Box>
            </Grid.Col>
            <Grid.Col xs={12} lg={7}>
              <Box className={classes.scollbox}>
                <Title order={4}>Privacy policy of "{currentApp.name}"</Title>
                <div dangerouslySetInnerHTML={{ __html: currentApp.policy }}  style={{overflow: "scroll"}} />
              </Box>
            </Grid.Col>
          </Grid>
        </section>
      </Stack>
    </>
  );
}
