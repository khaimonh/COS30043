<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-lg-8">
        <div class="bento-cell p-4 p-lg-5">
          <h2 class="display-text text-center mb-5">Candidate Intake Form</h2>
          
          <form @submit.prevent="handleSubmit" novalidate>
            <div class="row g-5">
              <div class="col-12">
                <fieldset class="p-4 rounded-4 border border-secondary border-opacity-25 bg-dark bg-opacity-50">
                  <legend class="h6 mb-4 text-muted-bento uppercase-tracked float-none w-auto px-3">Identity Profile</legend>
                  <div class="row g-4">
                    <div class="col-md-6">
                      <label class="small text-dim d-block mb-2">First Name</label>
                      <input type="text" class="form-control" v-model="form.firstName" :class="{'is-invalid': errors.firstName}" required />
                      <div class="invalid-feedback">{{ errors.firstName }}</div>
                    </div>
                    <div class="col-md-6">
                      <label class="small text-dim d-block mb-2">Last Name</label>
                      <input type="text" class="form-control" v-model="form.lastName" :class="{'is-invalid': errors.lastName}" required />
                      <div class="invalid-feedback">{{ errors.lastName }}</div>
                    </div>
                    <div class="col-12">
                      <label class="small text-dim d-block mb-2">Email Address</label>
                      <input type="email" class="form-control" v-model="form.email" :class="{'is-invalid': errors.email}" required />
                      <div class="invalid-feedback">{{ errors.email }}</div>
                    </div>
                  </div>
                </fieldset>
              </div>

              <div class="col-12">
                <fieldset class="p-4 rounded-4 border border-secondary border-opacity-25 bg-dark bg-opacity-50">
                  <legend class="h6 mb-4 text-muted-bento uppercase-tracked float-none w-auto px-3">System Credentials</legend>
                  <div class="row g-4">
                    <div class="col-md-6">
                      <label class="small text-dim d-block mb-2">Username</label>
                      <input type="text" class="form-control" v-model="form.username" :class="{'is-invalid': errors.username}" required />
                      <div class="invalid-feedback">{{ errors.username }}</div>
                    </div>
                    <div class="col-md-6">
                      <label class="small text-dim d-block mb-2">Password</label>
                      <input type="password" class="form-control" v-model="form.password" :class="{'is-invalid': errors.password}" required />
                      <div class="invalid-feedback">{{ errors.password }}</div>
                    </div>
                  </div>
                </fieldset>
              </div>

              <div class="col-12">
                <fieldset class="p-4 rounded-4 border border-secondary border-opacity-25 bg-dark bg-opacity-50">
                  <legend class="h6 mb-4 text-muted-bento uppercase-tracked float-none w-auto px-3">Logistics & Contact</legend>
                  <div class="row g-4">
                    <div class="col-12">
                      <label class="small text-dim d-block mb-2">Street Address</label>
                      <input type="text" class="form-control" v-model="form.streetAddress" />
                    </div>
                    <div class="col-md-6">
                      <label class="small text-dim d-block mb-2">Suburb</label>
                      <input type="text" class="form-control" v-model="form.suburb" />
                    </div>
                    <div class="col-md-6">
                      <label class="small text-dim d-block mb-2">Postcode</label>
                      <input type="text" class="form-control" v-model="form.postcode" :class="{'is-invalid': errors.postcode}" required />
                      <div class="invalid-feedback">{{ errors.postcode }}</div>
                    </div>
                  </div>
                </fieldset>
              </div>

              <div class="col-12">
                <fieldset class="p-4 rounded-4 border border-secondary border-opacity-25 bg-dark bg-opacity-50">
                  <legend class="h6 mb-4 text-muted-bento uppercase-tracked float-none w-auto px-3">Professional Classification</legend>
                  <div class="row g-4">
                    <div class="col-md-6">
                      <label class="small text-dim d-block mb-2">Date of Birth</label>
                      <input type="date" class="form-control" v-model="form.dateOfBirth" required />
                    </div>
                    <div class="col-md-6">
                      <label class="small text-dim d-block mb-2">Preferred Category</label>
                      <select class="form-select" v-model="form.jobCategory" required>
                        <option value="">-- Select --</option>
                        <option value="AI">AI</option>
                        <option value="Data Science">Data Science</option>
                        <option value="Web Development">Web Development</option>
                        <option value="Cybersecurity">Cybersecurity</option>
                        <option value="DevOps">DevOps</option>
                      </select>
                    </div>
                  </div>
                </fieldset>
              </div>
            </div>

            <div class="text-center mt-5 pt-4">
              <div class="form-check d-inline-block text-start me-4">
                <input class="form-check-input" type="checkbox" id="terms" v-model="form.termsAccepted" required />
                <label class="form-check-label small text-muted-bento" for="terms">
                  I certify the accuracy of these records.
                </label>
              </div>
              <button type="submit" class="btn btn-primary px-5 py-2">Transmit Application</button>
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
      form: {
        firstName: "",
        lastName: "",
        username: "",
        password: "",
        email: "",
        streetAddress: "",
        suburb: "",
        postcode: "",
        dateOfBirth: "",
        jobCategory: "",
        termsAccepted: false,
      },
      errors: {}
    };
  },
  methods: {
    validate() {
      this.errors = {};
      const { firstName, lastName, username, password, email, postcode } = this.form;
      const lettersOnly = /^[a-zA-Z\s]*$/;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const postCodeRegex = /^\d{4,5}$/;

      if (!firstName) this.errors.firstName = "First name is required";
      if (!lastName) this.errors.lastName = "Last name is required";
      if (!username) this.errors.username = "Username is required";
      if (!password) this.errors.password = "Password is required";
      if (!email) this.errors.email = "Email is required";
      if (!postcode) this.errors.postcode = "Postcode is required";

      if (firstName && !lettersOnly.test(firstName)) this.errors.firstName = "Only letters allowed";
      if (lastName && !lettersOnly.test(lastName)) this.errors.lastName = "Only letters allowed";

      if (username && username.length < 3) this.errors.username = "Too short (min 3 chars)";
      if (username && username.length > 15) this.errors.username = "Too long (max 15 chars)";
      
      if (password && password.length < 8) this.errors.password = "Security breach: min 8 chars";
      
      if (email && !emailRegex.test(email)) this.errors.email = "Invalid email format";
      
      if (postcode && !postCodeRegex.test(postcode)) this.errors.postcode = "Invalid postcode format";

      return Object.keys(this.errors).length === 0;
    },
    handleSubmit() {
      const handleSubmit = async (event) => {
        // event.preventDefault(); 

        const payload = {
          username: username,
          email: email
        };

        try {
          const response = await fetch('http://mercury.swin.edu.au/it000000/formtest.php', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const result = await response.json();
          console.log('Success:', result);

        } catch (error) {
          console.error('Error submitting form:', error);
        }
      };

          },
        },
      };
</script>

<style scoped>
.uppercase-tracked {
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.75rem;
  font-weight: 600;
}

fieldset {
  border: none !important;
}

legend {
  color: var(--text-muted);
  padding-left: 0;
}
</style>
