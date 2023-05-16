import { Avatar, Box, Button, Grid, Progress, RingProgress, ScrollArea, Stack, Text, Title, createStyles} from '@mantine/core'
import React, { Dispatch, SetStateAction, useState } from 'react'
import { useNavigate } from "react-router-dom";

interface Policy {
  [key: string]: number;
}

interface PolicyObject {
  id: string;
  name: string;
  image: string;
  policies: Policy;
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

      function combinePolicies(arr: PolicyObject[]): Policy {
        const combinedPolicies: Policy = {};
      
        for (let i = 0; i < arr.length; i++) {
          const policies = arr[i].policies;
          const policyKeys = Object.keys(policies);
      
          for (let j = 0; j < policyKeys.length; j++) {
            const key = policyKeys[j];
            const value = policies[key];
      
            if (combinedPolicies.hasOwnProperty(key)) {
              combinedPolicies[key] += value;
            } else {
              combinedPolicies[key] = value;
            }
          }
        }
      
        return combinedPolicies;
      }

      function calculateSumOfPolicies(policies: Policy) {
        let sum = 0;
        for (const key in policies) {
          if (typeof policies[key] === "number") {
            sum += policies[key];
          }
        }
        return sum;
      }

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
                    {Object.keys(combinePolicies(appData)).map(value => 
                    <>
                    <Grid.Col span={3}>
                            <Title order={6}>{value}</Title>
                        </Grid.Col>
                        <Grid.Col span={7} display="grid" sx={{alignContent: "center"}}>
                            <Progress value={(combinePolicies(appData)[value] / appData.length) * 100} size="xl" color={theme.colors.gray[4]}/>
                        </Grid.Col>
                        <Grid.Col span={2}>
                        <Title order={6}>{combinePolicies(appData)[value]} / {appData.length} Apps</Title>
                        </Grid.Col>
                    
                    </>    
                    )        
                    }
                   
                    </Grid>
                </ScrollArea>

            </Grid.Col>

          </Grid>
        </section>

        <section>
            <ScrollArea className={classes.scollbox}>
                
                {appData.map((value : PolicyObject) => 
                <Box p={10} sx={{borderRadius: 8}} bg="white"  mb={20}>
                    <Grid>
                        <Grid.Col span={1}  display="grid" sx={{alignContent: "center"}}>
                        <Avatar src={value.image} />
                           
                        </Grid.Col>
                        <Grid.Col span={1}  display="grid" sx={{alignContent: "center"}}>
                            <Title order={6}>{value.name}</Title>
                        </Grid.Col>
                        <Grid.Col span={5} display="grid" sx={{alignContent: "center"}}>
                                <Progress value={ (calculateSumOfPolicies(value.policies) / Object.keys(value.policies).length) * 100 } size="xl" color={theme.colors.gray[4]}/>
                        </Grid.Col>
                        <Grid.Col span={3}  display="grid" sx={{alignContent: "center"}}>
                            <Title order={6}>{calculateSumOfPolicies(value.policies)} / {Object.keys(value.policies).length} requirements fullfiled</Title>
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
