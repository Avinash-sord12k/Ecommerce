"use client";
import { operations } from "@/schema";
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { API_ENDPOINTS } from "./config";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: "",
    // headers: {
    //   Authorization: `Bearer ${localStorage.getItem("token")}`,
    // },
  }),
  endpoints: (builder) => ({
    login: builder.mutation<
      operations["login_user_api_v1_users_login_post"]["responses"]["200"]["content"]["application/json"],
      FormData
    >({
      query: (body: FormData) => {
        return {
          url: API_ENDPOINTS.login,
          params: {set_cookie: true},
          method: "POST",
          body,
        };
      },
    }),
  }),
});

export const { useLoginMutation } = authApi;
