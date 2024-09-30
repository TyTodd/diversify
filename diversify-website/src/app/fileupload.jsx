"use client";
// import { AiChat } from "@nlux/react";
// import { myCustomAdapter } from "./adapter.js";
import { useMemo, useEffect, useState } from "react";
// import "@nlux/themes/nova.css";
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

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const toast = useToast();
  const handleChange = (e) => {
    console.log("CHANGE");
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // const url = 'http://localhost:5000/';
    // const formData = new FormData();
    // formData.append('file', file);
    // formData.append('fileName', file.name);
    // const config = {
    //   headers: {
    //     'content-type': 'multipart/form-data',
    //   },
    // };
    // axios.post(url, formData, config).then((response) => {
    //   console.log(response.data);
    // });
    const data = new FormData();
    data.append("file", file);
    data.append("filename", file.filename);
    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: data,
      });
      if (!response.ok) {
        console.log(response);
        throw new Error("Bad request");
      } else {
        toast({
          title: `Successfully uploaded file`,
          status: "success",
          duration: 3000,
          isClosable: true,
        });
      }
    } catch (error) {
      console.error("Fetch error:", error);
      toast({
        title: "Error fetching data.",
        description: error.message,
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <div className="fileupload-container">
      {/* <div className="chatBot">
          <AiChat adapter={adapter} />
        </div> */}
      <label htmlFor="file-upload" className="sidebar-button">
        Upload Data
      </label>
      <input type="file" id="file-upload" onChange={handleChange} />
      <Flex width="100%" justifyContent="center" mt={2} mb={1}>
        {file?.name && (
          <Button onClick={handleSubmit}> Submit {file?.name} </Button>
        )}
      </Flex>
    </div>

    // <main className="flex min-h-screen flex-col items-center justify-between p-24">
    //   <div className="z-10 w-full max-w-3xl items-center justify-between font-mono text-sm lg:flex">
    //     <AiChat adapter={adapter} />
    //   </div>
    // </main>
  );
}
