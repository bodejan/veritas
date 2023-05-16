import { Avatar, Box, Button, Grid, Progress, RingProgress, ScrollArea, Stack, Text, Title, createStyles} from '@mantine/core'
import React, { useState } from 'react'
import { CircleCheck, CircleX } from 'tabler-icons-react';


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
  currentApp: PolicyObject;
}

const useStyles = createStyles((theme) => ({
    scollbox: {
        
       
        padding: 20,
        background: theme.colors.gray[1],
        borderRadius: 8,
    }
  }));

export default function AppDetail({currentApp}: OverviewProps) {
    const { classes, theme } = useStyles();


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
          <Title>Check privacy policies of {currentApp.name}</Title>
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
                    12 / 18
                </Text>
                }
            />
            </Grid.Col>
            <Grid.Col xs={12} lg={9}>
                <Box className={classes.scollbox}>
                <Grid p={10}>
                    <Grid.Col span={3} display="grid" sx={{alignContent: "center",justifyContent: "center"}}>
                            <Title order={6}>Category</Title>
                        </Grid.Col>
                        <Grid.Col span={2} display="grid" sx={{alignContent: "center",justifyContent: "center"}}>
                        <Title order={6}>Result</Title>
                            
                        </Grid.Col>
                        <Grid.Col span={7} display="grid" sx={{alignContent: "center", justifyContent: "center"}}>
                        <Title order={6}>Confidence</Title>
                        </Grid.Col>
                    </Grid>

                <Grid p={10}>
                    {Object.keys(currentApp.policies).map(value => 
                    <>
                    <Grid.Col span={3}>
                            <Text>{value}</Text>
                        </Grid.Col>
                        <Grid.Col span={2} display="grid" sx={{alignContent: "center", justifyContent: "center"}}>
                          {(currentApp.policies[value]) ? <CircleCheck color={theme.colors.green[6]} /> : <CircleX  color={theme.colors.red[6]}/> }
                            
                        </Grid.Col>
                        <Grid.Col span={6}>
                        <Progress value={80} size="xl" color={theme.colors.gray[4]}/>
                        </Grid.Col>

                        <Grid.Col span={1}>
                        90%
                        </Grid.Col>
                    
                    </>    
                    )        
                    }
                   
                    </Grid>
                </Box>

            </Grid.Col>

          </Grid>
        </section>
      </Stack>
    </>
  )
}
