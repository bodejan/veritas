// Import necessary modules from React and Mantine library
import React, { Dispatch, SetStateAction, forwardRef, useState, useEffect } from 'react';
import { MultiSelect, Avatar, Group, Text } from '@mantine/core';

// Define the shape of the data for each item in the MultiSelect
interface ItemProps {
  image: string;
  label: string;
  value: string;
  description: string;
}

// Utility function to map raw data to the shape required for each item in MultiSelect
function mapDataToItemProps(data: {
  id: string;
  name: string;
  logo_url: string;
}): ItemProps {
  return {
    image: data.logo_url,
    label: data.name,
    value: data.id,
    description: data.name, // Using 'name' as description, this can be changed if needed.
  };
}

// Define the props for the Searchbar component
interface SearchbarProps {
  setAppList: Dispatch<SetStateAction<string[]>>; // setAppList is a function to update the selected app list
}

// Define a custom component, SelectItem, for each item in the MultiSelect
const SelectItem = forwardRef<HTMLDivElement, ItemProps>(
  ({ image, label, description, ...others }: ItemProps, ref) => (
    <div ref={ref} {...others}>
      <Group>
        <Avatar src={image} /> {/* Display the Avatar image for each item */}
        <Text>{label}</Text> {/* Display the label (name) for each item */}
      </Group>
    </div>
  )
);

// Define the main Searchbar component that uses the MultiSelect
export function Searchbar({ setAppList }: SearchbarProps) {
  const [data, setData] = useState([]); // State to hold the data for MultiSelect options

  // Asynchronous function to fetch data from 'http://localhost:8000/get_db'
  const fetchData = async () => {
    try {
      const response = await fetch('http://localhost:8000/get_db');
      return await response.json(); // Return the fetched data as JSON
    } catch (error) {
      console.error('Error:', error);
    }
  };

  // useEffect hook is used to fetch data when the component mounts (empty dependency array)
  useEffect(() => {
    fetchData().then(item => {
      const convdata = JSON.parse(item).map(mapDataToItemProps); // Convert fetched data to ItemProps format
      setData(convdata); // Update the state with the fetched and converted data
    });
  }, []); // The empty dependency array ensures this effect runs only once when the component mounts

  return (
    <MultiSelect
      label="Search for Apps" 
      placeholder="Select apps you want to analyze" 
      itemComponent={SelectItem} 
      onChange={(values) => setAppList(values)} // Event handler for when selection changes, updating app list
      data={data} // Data to populate the MultiSelect options
      searchable // Enable search functionality for the MultiSelect dropdown
      nothingFound="Nobody here" 
      dropdownPosition="bottom"
      maxDropdownHeight={300} 
      limit={10} // Limit the number of visible options at a time in the dropdown
      filter={(value, selected, item) =>
        // Function to filter options based on the search query
        !selected && // Exclude already selected options from the filtered list
        (item.label?.toLowerCase().includes(value.toLowerCase().trim()) || // Match label with search query
          item.description.toLowerCase().includes(value.toLowerCase().trim())) // Match description with search query
      }
    />
  );
}
