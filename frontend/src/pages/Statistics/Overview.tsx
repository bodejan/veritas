import { Avatar, Box, Button, Grid, Progress, RingProgress, ScrollArea, Stack, Text, Title, createStyles} from '@mantine/core'
import React, { Dispatch, SetStateAction } from 'react'
import { useNavigate } from "react-router-dom";

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

interface OverviewProps{
  appData: PolicyObject[];
  setCurrentApp: Dispatch<SetStateAction<PolicyObject>>
}

const useStyles = createStyles((theme) => ({
    scollbox: {
        height: 300,
        padding: 20,
        background: theme.colors.gray[1],
        borderRadius: 8,
    }
  }));

export default function Overview({appData, setCurrentApp}: OverviewProps) {
    const { classes, theme } = useStyles();
    const navigate = useNavigate();

    const combinedPolicies = combinePolicies(appData);
    

      // Function for calculating how many Apps fullfill the each requirement
      function combinePolicies(arr: PolicyObject[]): Policy {
        const combinedPolicies: Policy = {};
      
        for (let i = 0; i < arr.length; i++) {
          const scores = arr[i].scores;
          const policyKeys = Object.keys(scores);
      
          for (let j = 0; j < policyKeys.length; j++) {
            const key = policyKeys[j];
            const value = scores[key];
      
            if (combinedPolicies.hasOwnProperty(key)) {
              combinedPolicies[key] += value;
            } else {
              combinedPolicies[key] = value;
            }
          }
        }
      
        return combinedPolicies;
      }

      // calculate the amout of requirements that are checked
      function calculateSumOfPolicies(scores: Policy) {
        let sum = 0;
        for (const key in scores) {
          if (typeof scores[key] === "number") {
            sum += scores[key];
          }
        }
        return sum;
      }

      const getProgressValue = (value: PolicyObject) => {
        const sumOfPolicies = calculateSumOfPolicies(value.scores);
        return (sumOfPolicies / Object.keys(value.scores).length) * 100;
      };

  return (
    <>
      <Stack p={20}>
        <section>
          <Title>Check privacy policies by app category</Title>
          <Text>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. </Text>
        </section>

        <Grid>
            <Grid.Col span={9}>

            </Grid.Col>
            <Grid.Col span={3} sx={{justifyContent: "end", display:"flex"}}>
                <Button color="dark">
                    Export data
                </Button>
            </Grid.Col>
        </Grid>
       

        <section>
          <Grid>
            <Grid.Col xs={12} lg={3}>
            <RingProgress
                sections={[{ value: 40, color: theme.colors.teal[7] }]}
                size={280}
                thickness={17}
                roundCaps
                label={
                <Text color={theme.colors.teal[7]} weight={700} align="center" size="40px">
                    Score
                </Text>
                }
            />
            </Grid.Col>
            <Grid.Col xs={12} lg={9}>
                <ScrollArea className={classes.scollbox}>
                    <Grid p={10}>
                    {Object.keys(combinedPolicies).map((value, index) => (
                    <React.Fragment key={index}>
                    <Grid.Col span={3}>
                            <Title order={6}>{value}</Title>
                        </Grid.Col>
                        <Grid.Col span={7} display="grid" sx={{alignContent: "center"}}>
                            <Progress value={(combinedPolicies[value] / appData.length) * 100} size="xl" color={theme.colors.gray[4]}/>
                        </Grid.Col>
                        <Grid.Col span={2}>
                        <Title order={6}>{combinedPolicies[value]} / {appData.length} Apps</Title>
                        </Grid.Col>
                    
                    </React.Fragment>    
                    ))        
                    }
                   
                    </Grid>
                </ScrollArea>

            </Grid.Col>

          </Grid>
        </section>

        <section>
            <ScrollArea className={classes.scollbox}>
                
                {appData.map((value : PolicyObject) => 
                <Box p={10} sx={{borderRadius: 8}} bg="white" mb={20} key={value.id}>
                    <Grid>
                        <Grid.Col span={1}  display="grid" sx={{alignContent: "center"}}>
                        <Avatar src={value.logo_url} />
                           
                        </Grid.Col>
                        <Grid.Col span={1}  display="grid" sx={{alignContent: "center"}}>
                            <Title order={6}>{value.name}</Title>
                        </Grid.Col>
                        <Grid.Col span={5} display="grid" sx={{alignContent: "center"}}>
                                <Progress value={ getProgressValue(value) } size="xl" color={theme.colors.gray[4]}/>
                        </Grid.Col>
                        <Grid.Col span={3}  display="grid" sx={{alignContent: "center"}}>
                            <Title order={6}>{calculateSumOfPolicies(value.scores)} / {Object.keys(value.scores).length} requirements fullfiled</Title>
                        </Grid.Col>
                        <Grid.Col span={2}  display="grid" sx={{alignContent: "center"}}>
                            <Button color="dark" variant='outline' onClick={() => {setCurrentApp(value); navigate("./app")}}>More Info</Button>
                        </Grid.Col>
                  
                    </Grid>  
                    </Box>
                )        
                }
                
                
            </ScrollArea>
        </section>
      </Stack>
    </>
  )
}
