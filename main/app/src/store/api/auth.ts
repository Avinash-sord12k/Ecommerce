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
          params: { set_cookie: true },
          method: "POST",
          body,
        };
      },
    }),
    session: builder.query<
      operations["get_user_me_api_v1_users_me_get"]["responses"]["200"]["content"]["application/json"],
      void
    >({
      query: () => {
        return {
          url: API_ENDPOINTS.me,
        };
      },
    }),
    logout: builder.mutation<
      operations["logout_user_api_v1_users_logout_get"]["responses"]["200"]["content"]["application/json"],
      void
    >({
      query: () => {
        return {
          url: API_ENDPOINTS.logout,
          method: "POST",
        };
      },
    }),
  }),
});

export const { useLoginMutation, useSessionQuery, useLogoutMutation } = authApi;
