import React, { useState } from 'react';
import { Box, Flex, Grid, RingProgress, Stack, Text, Title, createStyles, Modal, Paper, Slider, NumberInput, Button  } from '@mantine/core';
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

  const [modalVisible, setModalVisible] = useState(false);
  const [policyWeights, setPolicyWeights] = useState<Policy>(
    Object.keys(currentApp.scores).reduce((obj, item) => ({ ...obj, [item]: 1 }), {})
  );


  const calculateAverageScore = (appData: PolicyObject[], policyWeights: Policy): number => {
    let totalWeightedSum = 0;
    let totalWeight = 0;

    for (let i = 0; i < appData.length; i++) {
      const scores = appData[i].scores;
      const policyCount = Object.keys(scores).length;

      let weightedSum = 0;
      let weightSum = 0;

      for (const key in scores) {
        if (typeof scores[key] === 'number' && policyWeights[key]) {
          weightedSum += scores[key] * policyWeights[key];
          weightSum += policyWeights[key];
        }
      }

      const appWeightedAverage = weightSum > 0 ? weightedSum / weightSum : 0;
      totalWeightedSum += appWeightedAverage * policyCount;
      totalWeight += policyCount;
    }

    const averageScore = totalWeight > 0 ? totalWeightedSum / totalWeight : 0;
    return averageScore;
  };

  const openModal = () => {
    setModalVisible(true);
  };

  const closeModal = () => {
    setModalVisible(false);
  };

  const handleSliderChange = (policy: string, value: number) => {
    setPolicyWeights((prevWeights) => ({
      ...prevWeights,
      [policy]: value,
    }));
  };

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
