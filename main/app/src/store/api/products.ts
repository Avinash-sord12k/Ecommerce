"use client";
import { operations } from "@/schema";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_ENDPOINTS } from "./config";

export const productApi = createApi({
  reducerPath: "productApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "",
    // headers: {
    //   Authorization: `Bearer ${localStorage.getItem("token")}`,
    // },
  }),
  endpoints: (builder) => ({
    getProductsByCategory: builder.query({
      query: (
        params: operations["get_product_by_category_id_api_v1_product_get_by_category_id_get"]["parameters"]["query"]
      ) => {
        return { url: API_ENDPOINTS.getProductsByCategory, params };
      },
    }),
  }),
});

export const { useGetProductsByCategoryQuery } = productApi;
