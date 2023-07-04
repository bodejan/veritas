import React from 'react';
import { Box, Flex, Grid, RingProgress, Stack, Text, Title, createStyles } from '@mantine/core';
import { CircleCheck, CircleX } from 'tabler-icons-react';
import ExportData from './ExportData';

// Interfaces

// Interface for the scores object in the PolicyObject interface
interface Policy {
  [key: string]: number;
}

// Interface for the current app object
interface PolicyObject {
  id: string;
  name: string;
  logo_url: string;
  policy: string;
  scores: Policy;
  status: string;
}

// Interface for the props passed to the AppDetail component
interface OverviewProps {
  currentApp: PolicyObject;
}

// Create styles using the createStyles function from Mantine
const useStyles = createStyles((theme) => ({
  scollbox: {
    padding: 20,
    background: theme.colors.gray[1],
    borderRadius: 8,
  },
}));

// AppDetail component
export default function AppDetail({ currentApp }: OverviewProps) {
  // Get the classes and theme from the useStyles hook
  const { classes, theme } = useStyles();

  // Function to calculate the average score from the scores object
  const calculateScoreAverage = (scores: Policy): number => {
    const scoreValues = Object.values(scores);
    const sum = scoreValues.reduce((acc, score) => acc + score, 0);
    const average = sum / scoreValues.length;

    return average;
  };

  const score = (Number(calculateScoreAverage(currentApp.scores).toFixed(2))).toString().replace(/^(0.)+/, '')

  // Render component
  return (
    <>
      <Stack p={20}>
        <section>
          {/* Title and description */}
          <Title>Check privacy policy of {currentApp.name}</Title>
          <Text>
            Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore
            et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
            Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit
            amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam
            erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
          </Text>
        </section>

        {/* ExportData component */}
        <ExportData appData={[currentApp]} />

        <section>
          <Grid>
            <Grid.Col xs={12} lg={5}>
              <Flex justify="center">
                {/* RingProgress component to display the score average */}
                <RingProgress
                  sections={[{ value: Number(score), color: theme.colors.teal[7] }]}
                  size={280}
                  thickness={17}
                  roundCaps
                  label={
                    <Text color={theme.colors.teal[7]} weight={700} align="center" size="40px">
                      {score} %
                    </Text>
                  }
                />
              </Flex>

              <Box className={classes.scollbox}>
                <Grid p={10}>
                  <Grid.Col span={6} display="grid" sx={{ alignContent: 'center', justifyContent: 'center' }}>
                    {/* Title for the category */}
                    <Title order={6}>Category</Title>
                  </Grid.Col>
                  <Grid.Col span={6} display="grid" sx={{ alignContent: 'center', justifyContent: 'center' }}>
                    {/* Title for the result */}
                    <Title order={6}>Result</Title>
                  </Grid.Col>
                </Grid>

                <Grid p={10}>
                  {/* Render the scores for each category */}
                  {Object.keys(currentApp.scores).map((value) => (
                    <>
                      <Grid.Col span={6} display="grid">
                        {/* Display the category name */}
                        <Text>{value}</Text>
                      </Grid.Col>
                      <Grid.Col span={6} display="grid" sx={{ alignContent: 'center', justifyContent: 'center' }}>
                        {/* Display the result icon based on the score */}
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
                {/* Title for the privacy policy */}
                <Title order={4}>Privacy policy of "{currentApp.name}"</Title>
                {/* Render the policy HTML content */}
                <div dangerouslySetInnerHTML={{ __html: currentApp.policy }}  style={{overflow: "scroll"}} />
              </Box>
            </Grid.Col>
          </Grid>
        </section>
      </Stack>
    </>
  );
}
