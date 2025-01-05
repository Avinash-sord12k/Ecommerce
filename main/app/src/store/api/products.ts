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
    getProducts: builder.query<
      operations["get_products_api_v1_product_get"]["responses"]["200"]["content"]["application/json"],
      operations["get_products_api_v1_product_get"]["parameters"]["query"]
    >({
      query: (params) => {
        return { url: API_ENDPOINTS.getProducts, params };
      },
    }),
  }),
});

export const { useGetProductsQuery } = productApi;
