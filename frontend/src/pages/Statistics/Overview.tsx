import { Avatar, Box, Button, Flex, Grid, Progress, RingProgress, ScrollArea, Stack, Text, Title, createStyles } from '@mantine/core';
import React, { Dispatch, SetStateAction } from 'react';
import { useNavigate } from 'react-router-dom';
import ExportData from './ExportData';

// Interface for defining the structure of the policy scores
interface Policy {
  [key: string]: number;
}

// Interface for defining the structure of a policy object
interface PolicyObject {
  id: string;
  name: string;
  logo_url: string;
  policy: string;
  scores: Policy;
  status: string;
}

// Props interface for the Overview component
interface OverviewProps {
  appData: PolicyObject[];
  setCurrentApp: Dispatch<SetStateAction<PolicyObject>>;
}

const useStyles = createStyles((theme) => ({
  scollbox: {
    height: 300,
    padding: 20,
    background: theme.colors.gray[1],
    borderRadius: 8,
  },
}));

export default function Overview({ appData, setCurrentApp }: OverviewProps) {
  const { classes, theme } = useStyles();
  const navigate = useNavigate();
  const combinedPolicies = combinePolicies(appData);

  // Function for combining the policy scores of all apps
  function combinePolicies(arr: PolicyObject[]): Policy {
    const combinedPolicies: Policy = {};

    for (let i = 0; i < arr.length; i++) {
      const scores = arr[i].scores;
      const policyKeys = Object.keys(scores);

      for (let j = 0; j < policyKeys.length; j++) {
        const key = policyKeys[j];
        const value = scores[key];

        // Check if the combinedPolicies object already has the policy key
        if (combinedPolicies.hasOwnProperty(key)) {
          // If it exists, add the value to the existing score
          combinedPolicies[key] += value;
        } else {
          // If it doesn't exist, initialize it with the value
          combinedPolicies[key] = value;
        }
      }
    }

    return combinedPolicies;
  }

  // Function to calculate the sum of policy scores
  function calculateSumOfPolicies(scores: Policy) {
    let sum = 0;
    for (const key in scores) {
      if (typeof scores[key] === 'number') {
        sum += scores[key];
      }
    }
    return sum;
  }

  // Function to calculate the progress value for an app
  const getProgressValue = (value: PolicyObject) => {
    const sumOfPolicies = calculateSumOfPolicies(value.scores);
    return (sumOfPolicies / Object.keys(value.scores).length) * 100;
  };

  // Function to calculate the average score of all apps
  function calculateAverageScore(appData: PolicyObject[], decimalPlaces: number): number {
    let totalSum = 0;
    let totalCount = 0;

    for (let i = 0; i < appData.length; i++) {
      const sumOfPolicies = calculateSumOfPolicies(appData[i].scores);
      const policyCount = Object.keys(appData[i].scores).length;

      totalSum += sumOfPolicies;
      totalCount += policyCount;
    }

    const averageScore = totalCount > 0 ? totalSum / totalCount : 0;
    return Number(averageScore.toFixed(decimalPlaces));
  }

  return (
    <>
      <Stack p={20}>
        <section>
          <Title>Check privacy policies by app category</Title>
          <Text>
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et
            dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet
            clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet,
            consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
            sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
          </Text>
        </section>

        <ExportData appData={appData} />

        <section>
          <Grid>
            <Grid.Col xs={12} md={4}>
              <Flex justify="center" align="center">
                {/* Display the average score as a ring progress */}
                <RingProgress
                  sections={[{ value: calculateAverageScore(appData, 2) * 100, color: theme.colors.teal[7] }]}
                  size={280}
                  thickness={17}
                  roundCaps
                  label={
                    <Text color={theme.colors.teal[7]} weight={700} align="center" size="40px">
                      {calculateAverageScore(appData, 2) * 100} %
                    </Text>
                  }
                />
              </Flex>
            </Grid.Col>
            <Grid.Col xs={12} md={8}>
              <ScrollArea className={classes.scollbox}>
                <Grid p={10}>
                  {Object.keys(combinedPolicies).map((value, index) => (
                    <React.Fragment key={index}>
                      <Grid.Col span={3}>
                        {/* Display the policy name */}
                        <Title order={6}>{value}</Title>
                      </Grid.Col>
                      <Grid.Col span={7} display="grid" sx={{ alignContent: 'center' }}>
                        {/* Display the progress bar indicating the percentage of apps fulfilling the policy */}
                        <Progress
                          value={(combinedPolicies[value] / appData.length) * 100}
                          size="xl"
                          color={theme.colors.gray[4]}
                        />
                      </Grid.Col>
                      <Grid.Col span={2}>
                        {/* Display the count of apps fulfilling the policy */}
                        <Title order={6}>
                          {combinedPolicies[value]} / {appData.length} Apps
                        </Title>
                      </Grid.Col>
                    </React.Fragment>
                  ))}
                </Grid>
              </ScrollArea>
            </Grid.Col>
          </Grid>
        </section>

        <section>
          <ScrollArea className={classes.scollbox}>
            {/* Render the list of app data */}
            {appData.map((value: PolicyObject) => (
              <Box p={10} sx={{ borderRadius: 8 }} bg="white" mb={20} key={value.id}>
                <Grid>
                  <Grid.Col span={1} display="grid" sx={{ alignContent: 'center' }}>
                    {/* Display the app logo */}
                    <Avatar src={value.logo_url} />
                  </Grid.Col>
                  <Grid.Col span={2} display="grid" sx={{ alignContent: 'center' }}>
                    {/* Display the app name */}
                    <Title order={6}>{value.name}</Title>
                  </Grid.Col>
                  <Grid.Col span={3} display="grid" sx={{ alignContent: 'center' }}>
                    {/* Display the progress bar indicating the percentage of policies fulfilled by the app */}
                    <Progress value={getProgressValue(value)} size="xl" color={theme.colors.gray[4]} />
                  </Grid.Col>
                  <Grid.Col span={2} display="grid" sx={{ alignContent: 'center' }}>
                    {/* Display the count of requirements fulfilled by the app */}
                    <Title order={6}>
                      {calculateSumOfPolicies(value.scores)} / {Object.keys(value.scores).length} requirements fulfilled
                    </Title>
                  </Grid.Col>
                  <Grid.Col span={2} display="grid" sx={{ alignContent: 'center' }}>
                    {/* Display the app status */}
                    <Title order={6}>Status: {value.status}</Title>
                  </Grid.Col>
                  <Grid.Col span={2} display="grid" sx={{ alignContent: 'center' }}>
                    {/* Button to view more information about the app */}
                    <Button
                      color="dark"
                      variant="outline"
                      onClick={() => {
                        setCurrentApp(value);
                        navigate('./app');
                      }}
                    >
                      More Info
                    </Button>
                  </Grid.Col>
                </Grid>
              </Box>
            ))}
          </ScrollArea>
        </section>
      </Stack>
    </>
  );
}
