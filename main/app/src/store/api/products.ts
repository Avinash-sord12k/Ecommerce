"use client";
import { operations } from "@/schema";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_ENDPOINTS } from "./config";

export const productApi = createApi({
  reducerPath: "productApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "",
  }),
  endpoints: (builder) => ({
    getProductsByCategory: builder.query({
      query: (params: operations["get_products_api_v1_product_get"]["parameters"]["query"]) => {
        return { url: API_ENDPOINTS.getProducts, params };
      },
    }),
  }),
});

export const { useGetProductsByCategoryQuery } = productApi;
