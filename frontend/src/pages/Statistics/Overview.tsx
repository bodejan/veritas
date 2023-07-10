import { Avatar, Box, Button, Flex, Grid, Progress, RingProgress, ScrollArea, Stack, Text, Title, createStyles,  Modal, Paper, Slider, NumberInput  } from '@mantine/core';
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

  const [modalVisible, setModalVisible] = React.useState(false);
  const [policyWeights, setPolicyWeights] = React.useState<Policy>(Object.keys(appData[0].scores).reduce((obj, item) => ({ ...obj, [item]: 1 }), {}));

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

  function calculateSumOfPolicies(scores: Policy) {
    let sum = 0;
    for (const key in scores) {
      if (typeof scores[key] === 'number') {
        sum += scores[key];
      }
    }
    return sum;
  }
  
  function calculateAverageScore(appData: PolicyObject[], policyWeights: Policy): number {
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
  }

  // Function to calculate the progress value for an app
  const getProgressValue = (value: PolicyObject) => {
    const sumOfPolicies = calculateSumOfPolicies(value.scores);
    return (sumOfPolicies / Object.keys(value.scores).length) * 100;
  };

  // Function to calculate the average score of all apps
  
  //const weights = Object.keys(appData[0].scores).reduce((obj, item) => ({ ...obj, [item]: 1 }), {});
  const weights = policyWeights;
  const score = (calculateAverageScore(appData, weights) * 100).toFixed(2)

  //.toFixed(2)


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



  return (
    <>
      <Stack p={20}>
        <section>
          <Title>Overview</Title>
          <Text>
          On this page, you can find an overview of how well your selected apps fulfill the requirements of a privacy policy. If you want to check which specific requirements are fulfilled by a particular app, simply click on "More info."

          Additionally, you have the option to export the data by clicking on the "Export" button. This allows you to customize the information included in the export according to your preferences.
          </Text>
        </section>

        <Grid>
        <Grid.Col span={9}></Grid.Col>
        <Grid.Col span={3} sx={{ justifyContent: 'end', display: 'flex' }}>
          <Stack >
            <ExportData appData={appData} />

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
          <Grid.Col span={8} > 
          
              <Title order={6}>{policy}</Title>
           
          </Grid.Col>
          <Grid.Col span={4}>
            <NumberInput
            defaultValue={0.05}
            precision={2}
            min={0}
            max={1}
            step={0.05}
            value={policyWeights[policy]}
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
            <Grid.Col xs={12} md={4}>
              <Flex justify="center" align="center">
                {/* Display the average score as a ring progress */}
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
