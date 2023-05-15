import { Avatar, Box, Button, Flex, Grid, Image, Progress, RingProgress, ScrollArea, Stack, Text, Title, createStyles} from '@mantine/core'
import React, { useState } from 'react'

const useStyles = createStyles((theme) => ({
    scollbox: {
        maxHeight: 300,
       
        padding: 20,
        background: theme.colors.gray[1],
        borderRadius: 8,
    }
  }));

export default function Overview() {
    const { classes, theme } = useStyles();



    const [appdata, setAppdata] = useState(JSON.parse(JSON.stringify([
        {
          "id": "com.google.android.youtube",
          "name": "YouTube",
          "image": "https://play-lh.googleusercontent.com/lMoItBgdPPVDJsNOVtP26EKHePkwBg-PkuY9NOrc-fumRtTFP4XhpUNk_22syN4Datc=s96-rw",
          "policies": {
            "Data Categories": 0,
            "Processing Purpose": 1,
            "Data Recipients": 0,
            "Source of Data": 1,
            "Provision Requirement": 1,
            "Data Safeguards": 1,
            "Profiling": 1,
            "Storage Period": 0,
            "Adequacy Decision": 0,
            "Controllers Contact": 1,
            "DPO Contact": 1,
            "Withdraw Consent": 1,
            "Lodge Complaint": 1,
            "Right to Access": 1,
            "Right to Erase": 1,
            "Right to Restrict": 0,
            "Right to Object": 1,
            "Right to Data Portability": 0
          }
        },
        {
          "id": "facebook",
          "name": "Facebook",
          "image": "https://play.google.com/store/apps/details?id=com.facebook.katana",
          "policies": {
            "Data Categories": 0,
            "Processing Purpose": 1,
            "Data Recipients": 0,
            "Source of Data": 1,
            "Provision Requirement": 1,
            "Data Safeguards": 1,
            "Profiling": 1,
            "Storage Period": 0,
            "Adequacy Decision": 0,
            "Controllers Contact": 1,
            "DPO Contact": 1,
            "Withdraw Consent": 0,
            "Lodge Complaint": 0,
            "Right to Access": 0,
            "Right to Erase": 1,
            "Right to Restrict": 0,
            "Right to Object": 1,
            "Right to Data Portability": 0
          }
        }
      ])))

      interface Policy {
        [key: string]: number;
      }
      
      interface PolicyObject {
        id: string;
        name: string;
        image: string;
        policies: Policy;
      }
      
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
                sections={[{ value: 40, color: "teal" }]}
                size={280}
                thickness={17}
                roundCaps
                label={
                <Text color="teal" weight={700} align="center" size="40px">
                    12 / 18
                </Text>
                }
            />
            </Grid.Col>
            <Grid.Col xs={12} lg={9}>
                <ScrollArea className={classes.scollbox}>
                    <Grid p={10}>
                    {Object.keys(combinePolicies(appdata)).map(value => 
                    <>
                    <Grid.Col span={3}>
                            <Title order={6}>{value}</Title>
                        </Grid.Col>
                        <Grid.Col span={7} display="grid" sx={{alignContent: "center"}}>
                            <Progress value={(combinePolicies(appdata)[value] / appdata.length) * 100} size="xl" color={theme.colors.yellow[5]}/>
                        </Grid.Col>
                        <Grid.Col span={2}>
                        <Title order={6}>{combinePolicies(appdata)[value]} / {appdata.length} Apps</Title>
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
                
                {appdata.map((value : PolicyObject) => 
                    <Grid mb={20} p={10} sx={{borderRadius: 20}} bg={theme.colors.gray[0]}>
                        <Grid.Col span={2}>
                        <Avatar src={value.image} />
                           
                        </Grid.Col>
                        <Grid.Col span={2} >
                            <Title order={6}>{value.name}</Title>
                        </Grid.Col>
                        <Grid.Col span={4} display="grid" sx={{alignContent: "center"}}>
                                <Progress value={Object.keys(value.policies).length} size="xl" color={theme.colors.gray[5]}/>
                        </Grid.Col>
                        <Grid.Col span={2}>
                            <Title order={6}>{calculateSumOfPolicies(value.policies)} / {Object.keys(value.policies).length}</Title>
                        </Grid.Col>
                        <Grid.Col span={2}>
                            <Button color="dark" variant='outline'>More Info</Button>
                        </Grid.Col>
                    
                    </Grid>  
                )        
                }
                
                
            </ScrollArea>
        </section>
      </Stack>
    </>
  )
}
