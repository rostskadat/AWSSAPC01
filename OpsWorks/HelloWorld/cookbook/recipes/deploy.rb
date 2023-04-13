Chef::Log.info("********** deploy **********")
app = search(:aws_opsworks_app).first
app_path = "/srv/#{app['shortname']}"

if app["app_source"]["type"] == 'git'
  package "git" do
    # workaround for:
    # WARNING: The following packages cannot be authenticated!
    # liberror-perl
    # STDERR: E: There are problems and -y was used without --force-yes
    options "--force-yes" if node["platform"] == "ubuntu" && node["platform_version"] == "14.04"
  end
end

# Ref: https://supermarket.chef.io/cookbooks/application_javascript
application app_path do

  javascript "12.21.0"

  environment.update("PORT" => "80")
  environment.update(app["environment"])

  if app["app_source"]["type"] == 'git'
    Chef::Log.info("Cloning #{app['app_source']['url']} to #{app_path} ...")
    git app_path do
      repository app["app_source"]["url"]
      revision app["app_source"]["revision"]
    end
  else
    # Assuming 'archive'
    Chef::Log.info("Downloading Archive #{app[:app_source][:url]} and extracting to #{app_path} ...")
    tar_extract app["app_source"]["url"] do
      target_dir app_path
    end
  end

  link "#{app_path}/server.js" do
    to "#{app_path}/index.js"
  end

  #Chef::Log.info("SECRET_ARN: #{node[:deploy]['simplephpapp'][:environment_variables][:USER_ID]}")
  # Chef::Log.info("SECRET_ARN: #{environment['SECRET_ARN']}")

  Chef::Log.info("Installing #{app['shortname']} ...")
  npm_install
  npm_start do
    action [:stop, :enable, :start]
  end
end
