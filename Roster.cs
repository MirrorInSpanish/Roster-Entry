using System;
using System.Data;
using System.Windows.Forms;
using Npgsql;

namespace UserInfoForm
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
        }

        private void SubmitForm(object sender, EventArgs e)
        {
            string firstName = txtFirstName.Text.Trim();
            string lastName = txtLastName.Text.Trim();
            string ageText = txtAge.Text.Trim();
            string heightText = txtHeight.Text.Trim();

            // Validation for first name
            if (string.IsNullOrEmpty(firstName) || !IsAllLetters(firstName))
            {
                MessageBox.Show("Only letters are allowed for the first name.", "Input Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Validation for last name
            if (string.IsNullOrEmpty(lastName) || !IsAllLetters(lastName))
            {
                MessageBox.Show("Only letters are allowed for the last name.", "Input Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Validation for age
            if (!int.TryParse(ageText, out int age) || age <= 0 || age >= 100)
            {
                MessageBox.Show("Age must be a number between 1 and 99.", "Input Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Validation for height
            if (!float.TryParse(heightText, out float height) || height <= 0 || height >= 8)
            {
                MessageBox.Show("Height must be a number between 0 and 8 feet.", "Input Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Save data to PostgreSQL
            try
            {
                string connectionString = "Host=ep-lingering-truth-a5c1ym6f.us-east-2.aws.neon.tech;Username=Roster_owner;Password=8qTRoUFH5hxD;Database=Roster;SSL Mode=Require";
                using (var connection = new NpgsqlConnection(connectionString))
                {
                    connection.Open();
                    string query = "INSERT INTO users (first_name, last_name, age, height) VALUES (@firstName, @lastName, @age, @height)";
                    using (var command = new NpgsqlCommand(query, connection))
                    {
                        command.Parameters.AddWithValue("firstName", firstName);
                        command.Parameters.AddWithValue("lastName", lastName);
                        command.Parameters.AddWithValue("age", age);
                        command.Parameters.AddWithValue("height", height);
                        command.ExecuteNonQuery();
                    }
                }

                MessageBox.Show("User information saved to the Neon database!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);

                // Clear input fields
                txtFirstName.Clear();
                txtLastName.Clear();
                txtAge.Clear();
                txtHeight.Clear();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An error occurred: {ex.Message}", "Database Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private bool IsAllLetters(string input)
        {
            foreach (char c in input)
            {
                if (!char.IsLetter(c))
                    return false;
            }
            return true;
        }
    }
}
