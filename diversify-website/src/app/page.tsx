"use client";
import { useState } from "react";
import {
  Input,
  Button,
  Flex,
  Box,
  Text,
  Heading,
  Badge,
  useToast,
} from "@chakra-ui/react";

interface ApplicantCardProps {
  applicantName: string;
  score: number;
}

// const SearchBar = () => {
//   const [searchTerm, setSearchTerm] = useState("");

//   const handleSearch = async () => {
//     // Handle search logic here
//     // console.log('Searching for:', searchTerm);
//     try {
//       const response = await fetch(
//         `http://127.0.0.1:5000/search?applicant_name=${searchTerm}`
//       );
//       if (!response.ok) {
//         throw new Error("Network response was not ok");
//       }
//       const data = await response.json();
//       console.log("Fetched data:", data);
//       // Handle the fetched data as needed
//     } catch (error) {
//       console.error("Fetch error:", error);
//     }
//   };

//   return (
//     <Flex align="center" justify="center" mt={6} height="20%">
//       <Input
//         placeholder="Search an applicant name..."
//         value={searchTerm}
//         onChange={(e) => setSearchTerm(e.target.value)}
//         size="lg"
//         width="40%"
//         height="40px"
//         color="white" // Text color
//         bg="black" // Background color
//         _placeholder={{ color: "gray.400" }} // Placeholder color
//         borderColor="white" // Outline color
//         borderWidth="2px" // Border thickness
//         borderRadius="10px" // Rounded borders
//         fontSize="lg" // Text size
//         paddingLeft="10px"
//         _focus={{ borderColor: "teal.300", boxShadow: "0 0 0 1px teal.300" }} // Focus effect
//       />
//       <Button
//         colorScheme="teal"
//         onClick={handleSearch}
//         ml={10}
//         color="white" // Text color
//         bg="black" // Background color
//         _hover={{ bg: "gray.700" }} // Hover effect
//         fontSize="lg" // Button text size
//         // borderColor="white" // Outline color
//         // borderWidth="2px" // Border thickness
//         // borderRadius="10px" // Rounded borders
//       >
//         Search
//       </Button>
//     </Flex>
//   );
// };

const ApplicantCard: React.FC<ApplicantCardProps> = ({
  applicantName,
  score,
}) => {
  return (
    <Flex align="center" justify="center">
      <Box
        borderWidth="1px"
        borderRadius="lg"
        width="45%"
        overflow="hidden"
        p={5}
        bg="blackAlpha.700"
        color="white"
        boxShadow="md"
        padding="10px"
      >
        <Heading size="md" mb={2}>
          {applicantName}
        </Heading>
        <Text fontSize="lg">
          Score: <Badge colorScheme="green">{score}</Badge>
        </Text>
      </Box>
    </Flex>
  );
};

interface ApplicantData {
  name: string;
  score: number;
}

export default function Chat() {
  const [searchTerm, setSearchTerm] = useState("");
  const [applicantData, setApplicantData] = useState<ApplicantData | null>(
    null
  );
  const toast = useToast();
  const handleSearch = async () => {
    // Handle search logic here
    // console.log('Searching for:', searchTerm);
    try {
      console.log(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/search?applicant_name=${searchTerm}`
      );
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/search?applicant_name=${searchTerm}`
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      console.log("Fetched data:", data);
      setApplicantData(data);
      // Handle the fetched data as needed
    } catch (error) {
      console.error("Fetch error:", error);
      let errorMessage = "An unknown error occurred";
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      toast({
        title: "Error fetching data.",
        description: errorMessage,
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <div className="chatBot-container">
      {/* <div className="chatBot">
          <AiChat adapter={adapter} />
          
        </div> */}
      <Flex align="center" justify="center" mt={250} height="10%">
        <Heading as="h1" size="2xl" textAlign="center" mb={4} color="teal.500">
          Diversify
        </Heading>
      </Flex>
      <Flex align="center" justify="center" mt={50} height="10%">
        <Input
          placeholder="Search an applicant name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          size="lg"
          width="40%"
          height="40px"
          color="white" // Text color
          bg="black" // Background color
          _placeholder={{ color: "gray.400" }} // Placeholder color
          borderColor="white" // Outline color
          borderWidth="2px" // Border thickness
          borderRadius="10px" // Rounded borders
          fontSize="lg" // Text size
          paddingLeft="10px"
          _focus={{ borderColor: "teal.300", boxShadow: "0 0 0 1px teal.300" }} // Focus effect
        />
        <Button
          colorScheme="teal"
          onClick={handleSearch}
          ml={2}
          color="white" // Text color
          bg="black" // Background color
          _hover={{ bg: "gray.700" }} // Hover effect
          fontSize="lg" // Button text size
          // borderColor="white" // Outline color
          // borderWidth="2px" // Border thickness
          // borderRadius="10px" // Rounded borders
        >
          Search
        </Button>
      </Flex>
      {applicantData && (
        <ApplicantCard
          applicantName={applicantData?.name}
          score={applicantData?.score}
        />
      )}
    </div>
    // <main className="flex min-h-screen flex-col items-center justify-between p-24">
    //   <div className="z-10 w-full max-w-3xl items-center justify-between font-mono text-sm lg:flex">
    //     <AiChat adapter={adapter} />
    //   </div>
    // </main>
  );
}
