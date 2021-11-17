# About

The COVID-19 pandemic has created the largest disruption of education systems in history, affecting nearly 1.6 billion learners in more than 190 countries; school and learning space closures have impacted 94 per cent of the world’s student population. And, even before the pandemic, there were 3.6 billion people in the world without access to the Internet. This disruption in learning - especially those with pre-existing disparities in education and access - threatens to erase decades of progress, as closures of educational institutions hamper the provision of essential services to the entire community. The promise of future learning and living needs innovation and the internet to deliver quality education and services. 

How much will it cost to connect a school to the internet? How much bandwidth does a school need and what technology is best suited to deliver it? What will it cost to keep that school connected? And how will connectivity impact the community around that school?

The models contained here are used to quickly answer the above questions. Briefly they:

1. De-duplicate schools and consolidate multiple schools on the same site
2. Compute the school and local census if enrollment data doesn't exist
3. Determine the bandwidth needed
4. Selects a technology
5. Computes power requirements, and if grid power is unavailable or unreliable, sizes a solar and battery solution
6. Compute "overnight" cost to connect the school (labor and hardware). "Overnight" means that the work happens instantly, and doesn't account for the cost of capital or financing during the construction period. Also referred to as the Capital Expense (CapEx).
7. Computes annual costs to keep the school connected and all hardware maintained. Also referred to as the Operational Expense (OpEx).

Several assumptions have been made in building each model, especially around user needs and specific usage patterns. In addition, costing estimates are preliminary; models and inputs be refined with feedback from users and stakeholders.

# Installation

The simplest way to setup the Giga environemnt is to install minconda.
To do so, you can download the installer from the official Anaconda website [here](https://docs.conda.io/en/latest/miniconda.html).

Next, navigate to the Giga root directory and run: 

```bash
conda env create --name <your-environment> -f conda.yaml
```

You can call your environment anything you want, but something simple like `giga` is usually recommended. The above will install all the python/binary dependencies needed to run and develop Giga models. Once the environment is created, let's activate it by running:

```bash
conda activate <your-environment>
```

Let's install the giga library itself, by navigating the the giga root directory and running:

```bash
pip install -e .
```

Giga is installed and you should be ready to use the models! Please note that you will need to activate the giga environment every-time you open a new shell with `conda activate <your-environment>`. You can deactivate the environment by running `conda deactivate`.

You can check that the installation was succesful by running `pytest` from the root directory of the repository.

# Configuration

There are a number of ways to configure the Giga models. 
The reccomended way is to start with the google spreadsheet [here](https://docs.google.com/spreadsheets/d/1LsOLtcZG8FO9uF79H7Z_PdN6iHkuMyr5TXw3UllbahE/edit#gid=0) that defines the key model parameters. Note that there are quite a few parameters.
You are welcome to create a copy of this spreadsheet that you can reconfigure.
Please note, that you will need to use the google sheet ID of your new created document in order to pull the parameters from your copy of the sheet.
You can find additional instructions on how to do this in the example jupyter-notebook.
Next, you will need school data and (optionally) population data. 
You can use the tooling in the library to autmatically fetch relevant population data when you create a `giga` workspace. 
If school data is avaible, you can try out using the [sample notebook](https://drive.google.com/file/d/1tyHxSsp0G3_S1g0Zvwlm2QBj9hb7gEcR/view?usp=sharing) to generate visual outputs of the model. 

# Running
To run the `giga` models, you can use the jupyter-notebook [here](https://drive.google.com/file/d/1tyHxSsp0G3_S1g0Zvwlm2QBj9hb7gEcR/view?usp=sharing).

Additionally, you can use the command line interface made availble by the library to run the Giga models from the shell.
The command below will:

1. Create a new workspace (which downloads school, and default configuration data from the google sheet above) for Rwanda in `workspace/rwanda`
2. Run the full Giga model analysis
3. Write the results to `workspace/rwanda/results`

```bash
giga-analysis --school-data <your-school-data> --create-workspace workspace/rwanda --country Rwanda --results-directory workspace/rwanda/results
```

If you already have an existing workspace and want to run another analysis with new school data or updated Giga model parameters you can run the following command:

```bash
giga-analysis --school-data <your-school-data> --existing-workspace <existing-workspace-directory> --results-directory <desired-results-directory>
```

# About Giga: 
Some 3.6 billion people in the world do not have access to the Internet. The lack of access to the internet means exclusion, marked by the lack of access to the wealth of information available online, fewer resources to learn and grow, and limited opportunities for the most vulnerable children and youth to fulfill their potential. Closing the digital divide requires global cooperation, leadership, and innovation in finance and technology. 

Giga is a UNICEF-ITU global initiative to connect every school to the Internet and every young person to information, opportunity and choice. Connect with us by visiting https://gigaconnect.org and following us on [Twitter](https://twitter.com/Gigaconnect). 

# About ACTUAL:
ACTUAL gives infrastructure originators, investors, and other stakeholders confidence as they model and track the cost, impact, and outcomes of sustainable and net-zero infrastructure projects. Visit www.actualhq.com or [contact us](mailto:hello@actualhq.com) to learn more about how our digital-twin based models can help unlock new savings and revenue streams for your projects.

Follow ACTUAL on [Twitter](https://twitter.com/ActualHQ) and visit our [blog](http://blog.actualhq.com) to learn more about our other projects and perspectives.

# About UNICEF:
UNICEF promotes the rights and wellbeing of every child, in everything we do. Together with our partners, we work in 190 countries and territories to translate that commitment into practical action, focusing special effort on reaching the most vulnerable and excluded children, to the benefit of all children, everywhere.

For more information about UNICEF and its work for children, visit www.unicef.org.

Follow UNICEF on [Twitter](https://twitter.com/unicefmedia) and [Facebook](https://www.facebook.com/unicef/)
