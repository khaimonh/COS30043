<template>
  <div class="application-form-container container">
    <div class="row">
      <div class="col-12 col-md-8 offset-md-2">
        <div class="form-wrapper">
          <h2 class="display-text">Application Form</h2>

          <form @submit.prevent="handleSubmit">
            <fieldset>
              <legend>Personal Information</legend>

              <div class="row">
                <div class="col-6">
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
                </div>
                <div class="col-6">
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
                </div>
              </div>

              <div class="row">
                <div class="col-12">
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
                </div>
              </div>

              <div class="row">
                <div class="col-6">
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
                </div>
                <div class="col-6">
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
                </div>
              </div>

              <div class="row">
                <div class="col-12">
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
                </div>
              </div>
            </fieldset>

            <fieldset>
              <legend>Address Information</legend>

              <div class="row">
                <div class="col-12">
                  <label for="streetAddress">Street Address:</label>
                  <input
                    type="text"
                    id="streetAddress"
                    name="streetAddress"
                    v-model="streetAddress"
                    maxlength="40"
                  />
                </div>
              </div>

              <div class="row">
                <div class="col-6">
                  <label for="suburb">Suburb:</label>
                  <input
                    type="text"
                    id="suburb"
                    name="suburb"
                    v-model="suburb"
                    maxlength="20"
                  />
                </div>
                <div class="col-6">
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
                </div>
              </div>

              <div class="row">
                <div class="col-12">
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
                </div>
              </div>
            </fieldset>

            <fieldset>
              <legend>Additional Information</legend>

              <div class="row">
                <div class="col-12">
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
                </div>
              </div>

              <div class="row">
                <div class="col-12">
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
                </div>
              </div>
            </fieldset>

            <div class="row">
              <div class="col-12">
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
              </div>
            </div>

            <div class="row">
              <div class="col-12 text-center">
                <button type="submit">Submit</button>
              </div>
            </div>

            <div id="termsAndConditions" v-if="showTerms" class="row">
              <div class="col-12">
                <p>This is a placeholder for the Terms and Conditions. Please read carefully before submitting.</p>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
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
      console.log(this.$data);
    },
  },
};
</script>

<style scoped>
@import "../styles/ApplicationForm.css";
</style>
