"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { operations } from "@/schema";
import { useLoginMutation } from "@/store/api/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { cva } from "class-variance-authority";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { toast, Toaster } from "sonner";
import * as z from "zod";

type LoginType = operations["login_user_api_v1_users_login_post"];
type RequestObject = LoginType["requestBody"]["content"]["application/x-www-form-urlencoded"];

const PasswordMinLength = 6;

const loginSchema = z.object({
  grant_type: z.literal("password"),
  username: z.string().nonempty("Username is required."),
  password: z.string().min(PasswordMinLength, "Password must be at least 6 characters long."),
  scope: z.string().optional(), // Optional field
  client_id: z.string().optional(), // Optional field
  client_secret: z.string().optional(), // Optional field
});

function LoginForm() {
  const { register, handleSubmit, formState, reset } = useForm<RequestObject>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      grant_type: "password",
      scope: "",
      client_id: "",
      client_secret: "",
    },
    mode: "onChange",
  });

  const [Login, { isLoading }] = useLoginMutation();

  const router = useRouter();
  const onSubmit = async (data: RequestObject) => {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      formData.append(key, value ?? "");
    });

    try {
      await Login(formData)
        .unwrap()
        .then((res) => {
          console.log("🚀 ~ .then ~ res:", res);
          toast.success("Login successful.");
          localStorage.setItem("token", res.access_token);
          router.push("/");
        })
        .catch((error) => {
          console.error("An error occurred: ", error);
          toast.error(`An error occurred. ${error?.data?.detail}`, {
            action: (
              <Button
                type="button"
                onClick={() => {
                  reset();
                  toast.dismiss();
                }}
                size="sm"
              >
                retry
              </Button>
            ),
          });
        });
    } catch (error) {
      console.error("An error occurred: ", error);
    }
  };
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Toaster />
      <div className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="username">username</Label>
          <Input
            id="username"
            type="text"
            placeholder="m@example.com"
            required
            {...register("username")}
            className={cva({
              "border-red-500": formState.errors.username,
              "border-green-500": formState.dirtyFields.username && !formState.errors.username,
            })()}
          />
          <p className="text-sm text-gray-500">We&apos;ll never share your email with anyone else.</p>
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            required
            {...register("password")}
            className={cva({
              "border-red-500": formState.errors.password,
              "border-green-500": formState.dirtyFields.password && !formState.errors.password,
            })()}
          />
          <p className="text-sm text-gray-500">Passwords must be at least {PasswordMinLength} characters.</p>
        </div>
        <Button type="submit" className="w-full" disabled={isLoading}>
          Login
        </Button>
      </div>
    </form>
  );
}

export default LoginForm;
