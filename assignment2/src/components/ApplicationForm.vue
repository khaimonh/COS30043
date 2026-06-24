<template>
  <div class="application-form">
    <h2>Application Form</h2>

    <form @submit.prevent="handleSubmit">
      <fieldset>
        <legend>Personal Information</legend>

        <label for="firstName">First Name:</label>
        <input
          type="text"
          id="firstName"
          name="firstName"
          required
          v-model="firstName"
          :class="{ 'error': firstNameError }"
          pattern="[A-Za-z]+"
          title="Letters only"
        />
        <span class="error" v-if="firstNameError">{{ firstNameError }}</span>
        <br />

        <label for="lastName">Last Name:</label>
        <input
          type="text"
          id="lastName"
          name="lastName"
          required
          v-model="lastName"
          :class="{ 'error': lastNameError }"
          pattern="[A-Za-z]+"
          title="Letters only"
        />
        <span class="error" v-if="lastNameError">{{ lastNameError }}</span>
        <br />

        <label for="username">Username:</label>
        <input
          type="text"
          id="username"
          name="username"
          required
          v-model="username"
          :class="{ 'error': usernameError }"
          minlength="3"
        />
        <span class="error" v-if="usernameError">{{ usernameError }}</span>
        <br />

        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          required
          v-model="password"
          :class="{ 'error': passwordError }"
          minlength="8"
          title="Minimum 8 characters, must include at least one special character ($ % ^ & *)"
        />
        <span class="error" v-if="passwordError">{{ passwordError }}</span>
        <br />

        <label for="confirmPassword">Confirm Password:</label>
        <input
          type="password"
          id="confirmPassword"
          name="confirmPassword"
          required
          v-model="confirmPassword"
          :class="{ 'error': confirmPasswordError }"
        />
        <span class="error" v-if="confirmPasswordError">{{ confirmPasswordError }}</span>
        <br />

        <label for="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          required
          v-model="email"
          :class="{ 'error': emailError }"
        />
        <span class="error" v-if="emailError">{{ emailError }}</span>
        <br />
      </fieldset>

      <fieldset>
        <legend>Address Information</legend>

        <label for="streetAddress">Street Address:</label>
        <input
          type="text"
          id="streetAddress"
          name="streetAddress"
          v-model="streetAddress"
          maxlength="40"
        />
        <br />

        <label for="suburb">Suburb:</label>
        <input
          type="text"
          id="suburb"
          name="suburb"
          v-model="suburb"
          maxlength="20"
        />
        <br />

        <label for="postcode">Postcode:</label>
        <input
          type="text"
          id="postcode"
          name="postcode"
          required
          v-model="postcode"
          :class="{ 'error': postcodeError }"
          pattern="[0-9]{4}"
          title="Exactly 4 digits"
        />
        <span class="error" v-if="postcodeError">{{ postcodeError }}</span>
        <br />

        <label for="mobileNumber">Mobile Number:</label>
        <input
          type="text"
          id="mobileNumber"
          name="mobileNumber"
          required
          v-model="mobileNumber"
          :class="{ 'error': mobileNumberError }"
          pattern="04[0-9]{6}"
          title="Exactly 10 digits, must start with 04"
        />
        <span class="error" v-if="mobileNumberError">{{ mobileNumberError }}</span>
        <br />
      </fieldset>

      <fieldset>
        <legend>Additional Information</legend>

        <label for="dateOfBirth">Date of Birth:</label>
        <input
          type="date"
          id="dateOfBirth"
          name="dateOfBirth"
          required
          v-model="dateOfBirth"
          :class="{ 'error': dateOfBirthError }"
        />
        <span class="error" v-if="dateOfBirthError">{{ dateOfBirthError }}</span>
        <br />

        <label for="jobCategory">Preferred Job Category:</label>
        <select
          id="jobCategory"
          name="jobCategory"
          required
          v-model="jobCategory"
        >
          <option value="">-- Please select --</option>
          <option value="AI">AI</option>
          <option value="Data Science">Data Science</option>
          <option value="Web Development">Web Development</option>
        </select>
        <span class="error" v-if="jobCategoryError">{{ jobCategoryError }}</span>
        <br />
      </fieldset>

      <label for="terms">
        <input
          type="checkbox"
          id="terms"
          name="terms"
          required
          v-model="termsAccepted"
        />
        I agree to the
        <a href="#" onclick="showTerms()">Terms and Conditions</a>
      </label>

      <button type="submit">Submit</button>

      <div id="termsAndConditions" v-if="showTerms">
        <!-- TODO: -->
        <p>This is a placeholder for the Terms and Conditions. Please read carefully before submitting.</p>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      firstName: "",
      lastName: "",
      username: "",
      password: "",
      confirmPassword: "",
      email: "",
      streetAddress: "",
      suburb: "",
      postcode: "",
      mobileNumber: "",
      dateOfBirth: "",
      jobCategory: "",
      termsAccepted: false,
      firstNameError: "",
      lastNameError: "",
      usernameError: "",
      passwordError: "",
      confirmPasswordError: "",
      emailError: "",
      postcodeError: "",
      mobileNumberError: "",
      dateOfBirthError: "",
      jobCategoryError: "",
      showTerms: false,
    };
  },
  methods: {
    handleSubmit() {
      this.validateForm();
    },
    validateForm() {
      //TODO: Implement validation logic here. This is a placeholder.
      console.log(this.$data);
    },
  },
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
