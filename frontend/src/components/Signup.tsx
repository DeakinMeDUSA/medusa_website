import 'react-app-polyfill/ie11';
import * as React from 'react';
import { Field, Form, Formik, FormikHelpers } from 'formik';
import { RootStore } from "../index";
import { LoginValues } from "../pages/User";


export const LoginSignupForm = ({ store }: { store: RootStore }) => {
  return (
    <div>
      <h1>Sign in</h1>
      <Formik
        initialValues={{
          email: '',
          password: ''
        }}

        onSubmit={(
          values: LoginValues,
          { setSubmitting }: FormikHelpers<LoginValues>
        ) => {
          setTimeout(() => {
            let resp = store.userStore.handleLogin(values)
            setSubmitting(false);
          }, 500);
        }}
      >
        <Form>
          <label htmlFor="email">Email</label>
          <Field id="email" name="email" type="email" placeholder="John"/>

          <label htmlFor="password">Password</label>
          <Field id="password" name="password" placeholder="Doe" type="password"/>

          <button type="submit">Submit</button>
        </Form>
      </Formik>
    </div>
  );
};

//
// export const LoginSignupForm = (store: RootStore) => {
//   return (
//     <div>
//       <h1>Signup</h1>
//       <Formik
//         initialValues={{
//           firstName: '',
//           lastName: '',
//           email: '',
//         }}
//
//         onSubmit={(
//           values: Values,
//           { setSubmitting }: FormikHelpers<Values>
//         ) => {
//           setTimeout(() => {
//             alert(JSON.stringify(values, null, 2));
//             store.userStore.api.loginUser({ values })
//             setSubmitting(false);
//           }, 500);
//         }}
//       >
//         <Form>
//           <label htmlFor="firstName">First Name</label>
//           <Field id="firstName" name="firstName" placeholder="John"/>
//
//           <label htmlFor="lastName">Last Name</label>
//           <Field id="lastName" name="lastName" placeholder="Doe"/>
//
//           <label htmlFor="email">Email</label>
//           <Field
//             id="email"
//             name="email"
//             placeholder="john@acme.com"
//             type="email"
//           />
//
//           <button type="submit">Submit</button>
//         </Form>
//       </Formik>
//     </div>
//   );
// };
