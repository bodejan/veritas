import React, { Dispatch, SetStateAction, forwardRef, useState, useEffect } from 'react';
import { MultiSelect, Avatar, Group, Text } from '@mantine/core';

interface ItemProps {
  image: string;
  label: string;
  value: string;
  description: string;
}

function mapDataToItemProps(data: {
  id: string;
  name: string;
  logo_url: string;
}): ItemProps {
  return {
    image: data.logo_url,
    label: data.name,
    value: data.id,
    description: data.name,
  };
}

interface SearchbarProps {
  setAppList: Dispatch<SetStateAction<string[]>>;
}

const SelectItem = forwardRef<HTMLDivElement, ItemProps>(
  ({ image, label, description, ...others }: ItemProps, ref) => (
    <div ref={ref} {...others}>
      <Group>
        <Avatar src={image} />

        <div>
          <Text>{label}</Text>
          <Text size="xs" color="dimmed">
            {description}
          </Text>
        </div>
      </Group>
    </div>
  )
);

export function Searchbar({ setAppList }: SearchbarProps) {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/name');
        const convdata = (await response.json()).map(mapDataToItemProps);

        console.log(convdata);
        setData(convdata);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <MultiSelect
      label="Search for Apps"
      placeholder="Select apps you want to analyse"
      itemComponent={SelectItem}
      onChange={(values) => setAppList(values)}
      data={data}
      searchable
      nothingFound="Nobody here"
      dropdownPosition="bottom"
      maxDropdownHeight={300}
      limit={10}
      filter={(value, selected, item) =>
        !selected &&
        (item.label?.toLowerCase().includes(value.toLowerCase().trim()) ||
          item.description.toLowerCase().includes(value.toLowerCase().trim()))
      }
    />
  );
}
