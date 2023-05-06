require 'sinatra'
require 'tempfile'
require 'pp'
require 'fileutils'

set :bind, ENV['HOST'] || '0.0.0.0'
set :port, ENV['PORT'] || '8371'
set :public_folder, 'public'

get "/" do
  send_file File.join(settings.public_folder, 'index.html')
end

post '/generate' do
  # Generate a temp directory
  base_dir = Dir.mktmpdir('make-rpm-dir')
  spec = Tempfile.new(['rpm-spec', '.spec'])
  begin
    # Get the list of files
    if !params['file'] || params['file'].length == 0
      return 400, "No files!\n\n#{ params }"
    end

    files = params['file'].map do |f|
      {
        name: f['filename'].gsub(/[^a-zA-Z0-9._-]/m, ''),
        path: f['tempfile'].path
      }
    end

    if params['name'].nil? || params['summary'].nil? || params['version'].nil? || params['release'].nil? || params['description'].nil?
      return 400, "Missing argument!"
    end

    # Sanitize the parameters
    params['name'].gsub!(/[^a-zA-Z0-9._-]/m, '')
    params['summary'].gsub!(/[^a-zA-Z0-9._-]/m, '')
    params['version'].gsub!(/[^a-zA-Z0-9._-]/m, '')
    params['release'].gsub!(/[^a-zA-Z0-9._-]/m, '')

    # Generate a spec file
    spec.write <<EOF
Summary: #{ params['summary'] || 'no_summary' }
Name: #{ params['name']       || 'no_name' }
Version: #{ params['version'] || '1.0' }
Release: #{ params['release'] || '1.0' }
BuildArch: noarch
Group: Development/Libraries
License: n/a
Packager: BSidesSF CTF

%description
#{ params['description'] }

#disable automatic depedency generation
%define __find_requires %{nil}
%define _use_internal_dependency_generator 0

%define canonical_name #{params['name']}

%prep
# prepare temp build dir
rm -rf %{_builddir}/%{canonical_name}/
mkdir -p %{_builddir}/%{canonical_name}/

# Copy the files from staging
#{ files.map { |f| "cp '#{ f[:path] }' %{_builddir}/%{canonical_name}/#{ f[:name] }" }.join("\n") }

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/
cp -rvf $RPM_BUILD_DIR/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR

%files
#{ files.map { |f| "/%{canonical_name}/#{f[:name]}" }.join("\n") }
EOF

    spec.close()

    out = `rpmbuild -bb --define '_topdir #{ base_dir }' '#{ spec.path }' 2>&1`
    if out =~ /Wrote: (.*)$/
      outfile = $1

      content_type 'application/octet-stream'
      headers 'Content-Disposition' => "attachment; filename=\"#{ outfile.split(/\//).pop }\""

      return File.read(outfile)
    else
      $stderr.puts "rpmbuild error:"
      $stderr.puts out
      return "rpmbuild returned an error!"
    end
  rescue StandardError => e
    $stderr.puts e
    $stderr.puts e.backtrace
    return 500, "Something went wrong: #{ e }"
  ensure
    # Always delete the data
    FileUtils.rm_rf(base_dir)
    FileUtils.rm_rf(spec)
  end
end
