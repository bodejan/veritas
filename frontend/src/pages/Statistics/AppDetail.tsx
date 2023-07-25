import React, { useState } from 'react';
import { Box, Flex, Grid, RingProgress, Stack, Text, Title, createStyles, Modal, Paper, NumberInput, Button  } from '@mantine/core';
import { CircleCheck, CircleX } from 'tabler-icons-react';
import ExportData from '../../Components/ExportData';

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

  // State to manage the visibility of the modal
  const [modalVisible, setModalVisible] = useState(false);

  // State to manage the weights for each policy in the currentApp
  const [policyWeights, setPolicyWeights] = useState<Policy>(
    Object.keys(currentApp.scores).reduce((obj, item) => ({ ...obj, [item]: 1 }), {})
  );

// Function to calculate the average score based on appData and policyWeights
const calculateAverageScore = (appData: PolicyObject[], policyWeights: Policy): number => {
  // Initialize variables to store the total weighted sum and total weight
  let totalWeightedSum = 0;
  let totalWeight = 0;

  // Loop through each app in the appData array
  for (let i = 0; i < appData.length; i++) {
    // Get the scores object and the number of policies for the current app
    const scores = appData[i].scores;
    const policyCount = Object.keys(scores).length;

    // Initialize variables to store the weighted sum and weight sum for the current app
    let weightedSum = 0;
    let weightSum = 0;

    // Loop through each policy (key) in the scores object
    for (const key in scores) {
      // Check if the score for the policy is a number and if the policy has a weight assigned
      if (typeof scores[key] === 'number' && policyWeights[key]) {
        // If both conditions are true, calculate the weighted sum and weight sum
        weightedSum += scores[key] * policyWeights[key]; // Multiply the score by the policy weight and add to the weighted sum
        weightSum += policyWeights[key]; // Add the policy weight to the weight sum
      }
    }

    // Calculate the app's weighted average score based on the weight sum
    const appWeightedAverage = weightSum > 0 ? weightedSum / weightSum : 0;

    // Update the total weighted sum and total weight with the app's weighted average
    totalWeightedSum += appWeightedAverage * policyCount; // Multiply the app's weighted average by the policy count and add to the total weighted sum
    totalWeight += policyCount; // Add the policy count to the total weight
  }

  // Calculate the overall average score based on the total weight
  const averageScore = totalWeight > 0 ? totalWeightedSum / totalWeight : 0;

  // Return the calculated average score
  return averageScore;
};

  const openModal = () => {
    setModalVisible(true);
  };

  const closeModal = () => {
    setModalVisible(false);
  };

// Function to handle slider changes and update policyWeights state
const handleSliderChange = (policy: string, value: number) => {
  setPolicyWeights((prevWeights) => ({
    ...prevWeights,
    [policy]: value,
  }));
};

// Calculate the average score based on the currentApp data and policyWeights, and convert it to a percentage
const score = (calculateAverageScore([currentApp], policyWeights) * 100).toFixed(2);
  // Render component
  return (
    <>
      <Stack p={20}>
        <section>
          {/* Title and description */}
          <Title>Check privacy policy of {currentApp.name}</Title>
          <Text>
          On this page, you can find an overview of how well the app <b>{currentApp.name}</b> fulfill the requirements of a privacy policy. You can also find the privacy policy of the app on this page.

          Additionally, you have the option to export the data by clicking on the "Export" button. This allows you to customize the information included in the export according to your preferences.
          </Text>
        </section>

        <Grid>
        <Grid.Col span={9}></Grid.Col>
        <Grid.Col span={3} sx={{ justifyContent: 'end', display: 'flex' }}>
          <Stack >
        {/* ExportData component */}
        <ExportData appData={[currentApp]} />

        <Button variant="filled" color="cyan" onClick={openModal}>
        Adjust Weights
      </Button>

      </Stack>

      </Grid.Col>
      </Grid>

        <Modal opened={modalVisible} onClose={closeModal} title="Adjust Weights">
        <Paper p="lg">
          <Title order={6}>Adjust the weights for each policy:</Title>
          {Object.keys(policyWeights).map((policy) => (
            <div key={policy}>
              <Grid>
                <Grid.Col span={8}>
                  <Title order={6}>{policy}</Title>
                </Grid.Col>
                <Grid.Col span={4}>
                  <NumberInput
                    defaultValue={policyWeights[policy]}
                    min={0}
                    max={1}
                    step={0.05}
                    precision={2}
                    onChange={(value) => handleSliderChange(policy, Number(value))}
                  />
                </Grid.Col>
              </Grid>
            </div>
          ))}
          <Button fullWidth onClick={closeModal} mt="md">
            Apply
          </Button>
        </Paper>
      </Modal>
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
