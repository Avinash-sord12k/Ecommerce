"use client";
import { operations } from "@/schema";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_ENDPOINTS } from "./config";

export const cartApi = createApi({
  reducerPath: "cartApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "",
  }),
  tagTypes: ["cart"],
  endpoints: (builder) => ({
    getCarts: builder.query<
      operations["get_all_carts_api_v1_cart_get"]["responses"]["200"]["content"]["application/json"],
      operations["get_all_carts_api_v1_cart_get"]["parameters"]["query"]
    >({
      query: (params) => {
        return {
          url: API_ENDPOINTS.carts,
          method: "GET",
          params,
        };
      },
      // onQueryStarted: async ({ queryFulfilled }) => {
      //   try {
      //     const response = await queryFulfilled;
      //     console.log("🚀 ~ onQueryStarted: ~ response:", response);
      //   } catch (error) {}
      // },
      providesTags: ["cart"],
    }),
    createCart: builder.mutation<
      operations["create_cart_api_v1_cart_create_post"]["responses"]["201"]["content"]["application/json"],
      operations["create_cart_api_v1_cart_create_post"]["requestBody"]["content"]["application/json"]
    >({
      query: (body) => {
        return {
          url: API_ENDPOINTS.createCart,
          method: "POST",
          body,
        };
      },
      invalidatesTags: ["cart"],
    }),
    addItems: builder.mutation<
      operations["add_item_to_cart_api_v1_cart_add_item_post"]["responses"]["200"]["content"]["application/json"],
      operations["add_item_to_cart_api_v1_cart_add_item_post"]["requestBody"]["content"]["application/json"]
    >({
      query: (body) => {
        return {
          url: API_ENDPOINTS.addItemsInCart,
          method: "POST",
          body,
        };
      },
      invalidatesTags: ["cart"],
    }),
  }),
});

export const { useGetCartsQuery, useCreateCartMutation, useAddItemsMutation } = cartApi;
