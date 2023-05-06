import { Show } from "solid-js";
import { useParams, useRouteData } from "solid-start";
import { FormError } from "solid-start/data";
import {
  createServerAction$,
  createServerData$,
  redirect,
} from "solid-start/server";
import { createUserSession, findUserByName, getUser, login, register } from "~/db/session";

function validateUsername(username: string) {
  if (username.length < 3) {
    return `Usernames must be at least 3 characters long`;
  }
}

function validatePassword(password: string) {
  if (password.length < 3) {
    return `Passwords must be at least 3 characters long`;
  }
}

export function routeData() {
  return createServerData$(async (_, { request }) => {
    if (await getUser(request)) {
      throw redirect('/');
    }
    return {};
  });
}

export default function Login() {
  const data = useRouteData<typeof routeData>();
  const params = useParams();

  const [loggingIn, { Form }] = createServerAction$(async (form: FormData) => {
    const username = form.get("username");
    const password = form.get("password");
    const redirectTo = form.get("redirectTo") || "/";
    if (
      typeof username !== "string" ||
      typeof password !== "string" ||
      typeof redirectTo !== "string"
    ) {
      throw new FormError(`Form not submitted correctly.`);
    }

    const fields = { username, password };
    const fieldErrors = {
      username: validateUsername(username),
      password: validatePassword(password),
    };
    if (Object.values(fieldErrors).some(Boolean)) {
      throw new FormError("Fields invalid", { fieldErrors, fields });
    }

    let user = await findUserByName(username);
    if (user !== undefined) {
      if (await login(user, password) !== undefined) {
        return createUserSession(`${user.id}`, redirectTo);
      }
      throw new FormError(`Invalid password`, { fields });
    } else {
      user = await register(username, password);
      if (!user) {
        throw new FormError(`Unable to create a new user.`, { fields });
      }
      return createUserSession(`${user.id}`, redirectTo);
    }
  });

  return (
    <main>
      <h1>Login</h1>
      <Form>
        <input
          type="hidden"
          name="redirectTo"
          value={params.redirectTo ?? "/"}
        />
        <div>
          <label for="username-input">Username</label>
          <input name="username" placeholder="kody" />
        </div>
        <Show when={loggingIn.error?.fieldErrors?.username}>
          <p role="alert">{loggingIn.error.fieldErrors.username}</p>
        </Show>
        <div>
          <label for="password-input">Password</label>
          <input name="password" type="password" placeholder="twixrox" />
        </div>
        <Show when={loggingIn.error?.fieldErrors?.password}>
          <p role="alert">{loggingIn.error.fieldErrors.password}</p>
        </Show>
        <Show when={loggingIn.error}>
          <p role="alert" id="error-message">
            {loggingIn.error.message}
          </p>
        </Show>
        <button type="submit">{data() ? "Login" : ""}</button>
      </Form>
    </main>
  );
}
